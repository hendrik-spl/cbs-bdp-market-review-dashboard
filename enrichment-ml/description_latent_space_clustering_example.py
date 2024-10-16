import time
import re
import requests
import polars as pl
import streamlit as st
from tqdm import tqdm

import numpy as np
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
from umap import UMAP

from sklearn.cluster import KMeans
from sklearn import metrics

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

def hf_query(payload):
	if payload['inputs'] is None:
		return None
	
	response = requests.post(st.secrets['hf_url'], headers={"Authorization": f"Bearer {st.secrets['hf_api']}"}, json=payload)
	return response.json()

def set_embedding(description: str = None):
        if description is None:
            return None
        else:
            embedding = hf_query({"inputs": description,})
            if isinstance(embedding, list):
                return embedding
            else:
                time.sleep(30)
                return set_embedding(description)

def latent_space_clustering(embeddings: pl.Series = None, verbose: bool = False, N_random_runs: int = 10, K_clusters: int = 10, K_clusters_start: int = 6):

    # Latent representation
    ## Structure data
    embeddings_X = np.array(embeddings.to_list())

    ## Define all models
    dim_models = [PCA(n_components=2), TruncatedSVD(n_components=2),]
    for p in range(5, K_clusters_start+K_clusters):
        dim_models.append(TSNE(n_components=2, perplexity = p, n_iter = 5000))
        dim_models.append(UMAP(n_components=2, n_neighbors=p))
    
    N_models = len(dim_models)

    ## Storage
    reduced_embeddings_list_m = np.zeros((N_models, len(embeddings_X), 3))
    silhoutte_score_m = np.zeros(N_models)
    
    ## Loop through models
    for i_model, dim_model in enumerate(tqdm(dim_models, desc = "Finding best latent clustering...")):

        # storage
        reduced_embeddings_r = np.zeros((N_random_runs, len(embeddings_X), 3))
        silhoutte_score_r = np.zeros(N_random_runs)

        ## Loop through random iterations:
        for i_random in range(N_random_runs):

            # storage
            reduced_embeddings_k = np.zeros((K_clusters, len(embeddings_X), 3))
            silhoutte_score_k = np.zeros(K_clusters)

            # dimensionality reduction
            reduction_model = dim_model
            reduced_embeddings = reduction_model.fit_transform(embeddings_X)

            # clustering
            for k in range(K_clusters):
                clustering = KMeans(n_clusters = k + K_clusters_start, n_init = 10).fit(reduced_embeddings)
                labels = clustering.labels_.astype('int')
                silhoutte_score_k[k] = metrics.silhouette_score(embeddings_X, labels, metric = 'euclidean')
                reduced_embeddings_k[k, :, : ] = np.vstack((reduced_embeddings.T, labels)).T
            
            # Find best reduced representation and labels for random run i
            silhoutte_score_r[i_random] = np.max(silhoutte_score_k)
            reduced_embeddings_r[i_random, :, :] = reduced_embeddings_k[np.argmax(silhoutte_score_k), :, :]

        # Find best reduced representation and labels for model i_model
        silhoutte_score_m[i_model] = np.max(silhoutte_score_r)
        reduced_embeddings_list_m[i_model, :, :] = reduced_embeddings_r[np.argmax(silhoutte_score_r), :, :]

    best_representation = reduced_embeddings_list_m[np.argmax(silhoutte_score_m), :, :]
    
    if verbose:
        print(f"Best representation given by {len(np.unique(best_representation[:, 2]))} clusters using reduction model {dim_models[np.argmax(silhoutte_score_r)]}")

    return best_representation

def extract_best_word(data: pl.DataFrame, labels_col: str = "labels_all"):
    optimal_k = len(data[labels_col].unique())

    # Extract the best words for each cluster
    stop_words = stopwords.words('english')
    corpus = [" ".join(data.select(
        pl.concat_str(['Organization Industries', 'Organization Description'], separator = " ",)
        )['Organization Industries'].filter(data[labels_col] == k).apply(lambda x: '' if x == None else x, skip_nulls = False).to_list()) for k in range(int(optimal_k))]

    ## pre-processing corpus
    corpus = [re.sub('[^A-Za-z2 ]+', '', string.lower()) for string in corpus]
    corpus = [' '.join([word for word in string.split(" ") if word not in stop_words]) for string in corpus]
    corpus = [string.replace("artificial intelligence", "ai") for string in corpus]
    corpus = [string.replace("machine learning", "ml") for string in corpus]
    corpus = [string.replace("information technology", "it") for string in corpus]
    corpus = [string.replace("  ", " ") for string in corpus]

    # tfidf
    vectorizer = TfidfVectorizer()
    tfidf_scores = vectorizer.fit_transform(corpus)
    best_word = vectorizer.get_feature_names_out()[np.argmax(tfidf_scores.toarray(), axis=1)]

    return best_word
