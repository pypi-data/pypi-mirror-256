from ..src.fixpoint import FixpointClient, ThumbsReaction

def main():
  # Make sure that the enviroment variables set:
  # - `FIXPOINT_API_KEY` is set to your Fixpoint API key
  # - `OPENAI_API_KEY` is set to your normal OpenAI API key
  # Create a FixpointClient instance (uses the FIXPOINT_API_KEY env var)
  client = FixpointClient()

  # Call create method on FixpointClient instance
  openai_response, fixpoint_input_log_response, fixpoint_output_log_response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "What are you?"
      }
    ]
  )

  # If you make multiple calls to an LLM that are all part of the same "trace"
  # (e.g. a multi-step chain of prompts), you can pass in a trace_id to
  # associate them together.
  openai_response2, fixpoint_input_log_response2, fixpoint_output_log_response2 = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "What are you?"
      }
    ],
    trace_id="some-trace-id"
  )

  # Record user feedback. One user giving a thumbs up to a log, the other giving a thumbs down.
  # The `user_id` you specify should be your own system's user identifier for
  # whoever gave the feedback.
  client.fixpoint.user_feedback.create({
    "likes": [
      {
        "log_name": fixpoint_input_log_response['name'],
        "thumbs_reaction": ThumbsReaction.THUMBS_UP,
        "user_id": "some-user-id"
      },
      {
        "log_name": fixpoint_input_log_response2['name'],
        "thumbs_reaction": ThumbsReaction.THUMBS_DOWN,
        "user_id": "some-other-user-id",
      }
    ]
  })

  # Record an attribute
  client.fixpoint.attributes.create({
    "log_attribute": {
      "log_name": fixpoint_input_log_response['name'],
      "key": "conversion",
      "value": "true",
    }
  })

main()
