# Ensure that all the required dependencies are installed
# pip install accelerate # Used to accelerate the process
# pip install torch
# pip install transformers

import torch
import os
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline, logging
logging.set_verbosity_error() # to skip the message after initializing the model

# We need to specify the device, whether we use a gpu or a cpu
# here we are also selecting the data type
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32


def get_transcription(filename: str):
    # If file name is not a string, the function should raise an error
    if not isinstance(filename, str):
        raise TypeError("Please enter a filename of type String")

    # Now, we try to get the transcript from the audio file
    try:
        model_id = "Aditya02/Vistar_Marathi_Model"  # model from huggingface
        # Model initialization
        model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, low_cpu_mem_usage=True, torch_dtype=torch_dtype)
        model.to(device)  # moves the model to the device(GPU or CPU)
        processor = AutoProcessor.from_pretrained(model_id)  # initializes the model associated with the model

        # Creating a pipeline
        pipe = pipeline(
            'automatic-speech-recognition',
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,  # duration of each audio should not be greater than 30s
            batch_size=16,
            torch_dtype=torch_dtype,  # data type which is selected based on device
            device=device  # cuda:0 if available elso cpu
        )

        result = pipe(filename)
        model_output = result['text']

        transcription = model_output
        return transcription

    except FileNotFoundError as fe:
        # Catching error if the given file is not found
        raise FileNotFoundError(f"File not found: {fe}")
    except RuntimeError as re:
        # Catching any unexpected error
        raise RuntimeError(f'Error while transcription: {re}')
