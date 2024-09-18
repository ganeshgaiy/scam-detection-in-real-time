# Scam call detection in real time using an on-device LLM

The main goal of this project is to build a system capable of classifying if a real time phone conversation is a scam. 

# Proposed workflow:
1. The feature is integrated into your phone's native calling app or a separate security app.
2. As you receive a call, the app listens to the conversation in real-time using your phone's microphone.
3. The audio is converted into text using Automatic Speech Recognition (ASR) technology.
4. Relevant linguistic features are extracted from the transcribed text, as described in the previous response.
5. The trained model analyzes these features to determine the likelihood of the call being a scam.
6. If the predicted probability of the call being a scam exceeds a certain threshold, you'll receive a notification or alert, often displayed directly on your phone's screen during the call.

This repository will also contain information on fine tuning Mistral 7B parameter model using a dataset that was created out of subreddits like r/scams, r/phishing etc.,

