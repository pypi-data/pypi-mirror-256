# Fixpoint Python SDK

The `FixpointClient` wraps the OpenAI API Client. You can call it just like OpenAI API Client. The sdk will intercept calls to certain OpenAI APIs, record input / outputs and forward that information to Fixpoint's api server.

## Usage

To use the sdk make sure that you have the following variables set in your environment: `FIXPOINT_API_KEY` and `OPENAI_API_KEY`.

## Virtual Env

To create a virtual environment called `venv` from your terminal run `python3 -m venv venv`.

### Activate

`source venv/bin/activate`

### Install packages

To install packages from `requirements.txt` in your virtual environment using `pip` run: `pip install -r requirements.txt`

### Deactivate

`deactivate`

## Examples

You can find examples of how to use the API in `examples`.
