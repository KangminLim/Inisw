import numpy as np

import torch as th
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_sequence

import tensorflow.compat.v2 as tf
import tensorflow_io as tfio
import tensorflow_hub as hub

import soundfile as sf
import sklearn
import json

import tqdm
import random
import pathlib
import itertools
import collections

import os
import cv2
import remotezip as rz

from nltk.corpus import stopwords #불용어 제거
from nltk.tokenize import sent_tokenize, word_tokenize, regexp_tokenize # 토큰화 모듈
import re
import numpy as np

import time
from tqdm import notebook
from transformers import AutoTokenizer

import nltk  # 불용어 처리
nltk.download('stopwords')
nltk.download('punkt')

import gensim
from gensim.models.keyedvectors import KeyedVectors

import tqdm
import random
import pathlib
import itertools
import collections

import os
import cv2
import remotezip as rz

from backbone.use_qvhighlights import use_qvhighlight
from backbone.audio_converter import converter

from backbone.video import video_embedding
from backbone.audio import audio_embedding
from text import text_embedding

# Hyperparameter
video_path = "./dataset/raw_videos"
audio_path = "./dataset/raw_audios"

data_path = ["dataset/data/highlight_train_release.jsonl",
             "dataset/data/highlight_test_release.jsonl",
             "dataset/data/highlight_val_release.jsonl"]

mini_batch_size = 32

T_v = 32
W = 200
H = 200

T_a = 153600


# query와 video 추출
Video_file_name = use_qvhighlight(data_path, mini_batch_size)


# video에서 audio 추출
converter(Video_file_name, video_path, audio_path)


# feature 추출
video = video_embedding(video_path, Video_file_name, T_v, H, W)
video.extract()

audio = (audio_path, Video_file_name, T_a)
audio.extract()

text = text_embedding(Video_file_name)
text.extract()