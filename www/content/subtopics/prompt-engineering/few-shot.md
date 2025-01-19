---
title: Few-Shot Prompting
weight: 60
description: Few-Shot Prompting is a technique where the model is provided with a few examples of input-output pairs within the prompt to guide its behavior on a task.
---
Few-Shot Prompting is a technique where the model is provided with a few examples of input-output pairs within the prompt to guide its behavior on a task. These examples serve as implicit demonstrations, enabling the model to generalize patterns and perform the desired task without requiring explicit fine-tuning. Few-Shot Prompting is effective for tasks such as classification, translation, and text generation, leveraging in-context learning to improve accuracy and reduce ambiguity while minimizing the need for extensive labeled data.

<!-- more -->

Here are three detailed examples of **Few-Shot Prompting**, ranging from simple to advanced and complex:

---

### 1. **Simple Example: Sentiment Classification**
   - **Task**: Classify the sentiment of customer feedback as positive, negative, or neutral.
   - **Prompt**:
     ```
     Classify the sentiment of the following text as positive, negative, or neutral.

     Text: "The product is terrible."  
     Sentiment: Negative  

     Text: "Super helpful, worth it!"  
     Sentiment: Positive  

     Text: "It doesn't work!"  
     Sentiment:
     ```
   - **Output**:
     ```
     Negative
     ```
   - **Explanation**: By providing two labeled examples (positive and negative), the model learns the pattern for classifying sentiment and applies it to the new input ("It doesn't work!"). This improves accuracy compared to zero-shot prompting.

---

### 2. **Intermediate Example: Structured Data Extraction**
   - **Task**: Extract technical specifications from product descriptions and format them in JSON.
   - **Prompt**:
     ```
     Extract the technical specifications from the text below in JSON format.

     Input: "Google Nest Wifi, network speed up to 1200Mbps, 2.4GHz and 5GHz frequencies, WP3 protocol"  
     Output: {  
       "product": "Google Nest Wifi",  
       "speed": "1200Mbps",  
       "frequencies": ["2.4GHz", "5GHz"],  
       "protocol": "WP3"  
     }  

     Input: "Google Pixel 7, 5G network, 8GB RAM, Tensor G2 processor, 128GB of storage, Lemongrass"  
     Output:
     ```
   - **Output**:
     ```
     {  
       "product": "Google Pixel 7",  
       "network": "5G",  
       "ram": "8GB",  
       "processor": "Tensor G2",  
       "storage": "128GB",  
       "color": "Lemongrass"  
     }
     ```
   - **Explanation**: The prompt includes an example with structured JSON output that demonstrates how to extract and format product details. The model uses this pattern to produce a consistent output for the new input.

---

### 3. **Advanced Example: Travel Itinerary Generation**
   - **Task**: Generate concise travel itineraries based on destination and trip type.
   - **Prompt**:
     ```
     Create a travel itinerary based on the destination and trip type provided.

     Destination: Tokyo, Japan  
     Trip Type: Cultural Exploration  
     Itinerary: A 5-day immersion in Tokyo's blend of tradition and modernity. Visit ancient temples like Senso-ji, then explore futuristic districts like Akihabara. Experience a tea ceremony, try hands-on workshops in traditional crafts, and end with a day trip to Mt. Fuji for breathtaking views of Japan's iconic landmark.

     Destination: Costa Rica  
     Trip Type: Eco-Adventure  
     Itinerary: 7 days of natural wonders and adrenaline rushes. Start in the Arenal Volcano area for hiking and zip-lining, then head to Monteverde Cloud Forest for canopy walks and wildlife spotting. Finish at Manuel Antonio National Park, combining rainforest exploration with relaxation on pristine beaches.

     Destination: Rome, Italy  
     Trip Type: Culinary Journey  
     Itinerary:
     ```
   - **Output**:
     ```
     A 6-day feast for the senses in the Eternal City. Begin with a pasta-making class, followed by guided food tours through trendy Trastevere and historic Jewish Ghetto. Visit local markets, enjoy wine tasting in the Roman countryside, and cap off the trip with a Michelin-starred dining experience.
     ```
   - **Explanation**: The examples provide clear formatting and style for travel itineraries based on destination and trip type. The model generalizes this pattern to generate a new itinerary for Rome.

---

### Summary
- **Simple Example** focuses on sentiment classification using short phrases.
- **Intermediate Example** demonstrates structured data extraction with JSON formatting.
- **Advanced Example** showcases creative content generation by crafting tailored travel itineraries.

These examples highlight how Few-Shot Prompting leverages multiple examples to guide AI models in recognizing patterns and producing accurate outputs across a range of tasks.

## Citations
- [1] https://learnprompting.org/docs/basics/few_shot
- [2] https://www.ibm.com/think/topics/few-shot-prompting
- [3] https://www.prompthub.us/blog/the-few-shot-prompting-guide
- [4] https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/few-shot-examples
- [5] https://www.datacamp.com/tutorial/few-shot-prompting