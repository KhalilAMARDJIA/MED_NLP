
# See this VIDEO: https://youtube.com/watch?v=W8ZPQOcHnlE&feature=shares

# to install torch-gpu one should:

# check the latest (or not) versions and compatible cuda version: https://pytorch.org/get-started/locally/, at this moment it is 11.7.

# for windows e.g.: pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117


# download and install cuda of the established version above) step (https://developer.nvidia.com/cuda-toolkit-archive). That depends on the gpu, if any problems you may download older versions or maybe you have it installed? then you can check version manually in the command line: nvcc --version.

# for this example CUDA Toolkit 11.7.0 (May 2022), Versioned Online Documentation



python -m venv .env
.env\Scripts\activate
pip install -U pip setuptools wheel
pip install -U 'spacy[cuda117,transformers,lookups]' #cuda version nvcc --version
python -m spacy download en_core_web_trf
pip install  https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_core_sci_md-0.5.1.tar.gz #scispacy medium model

pip install -r .\requirements.txt
