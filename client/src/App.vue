<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const question = ref('')
const answer = ref('')
const isLoading = ref(false)

const API_URL = 'https://kw5uzneejhbujvqypkrcsi4wji0dodqu.lambda-url.eu-central-1.on.aws/'

async function ask() {
  const questionText = question.value.trim()
  
  if (!questionText) {
    alert('Please enter a question.')
    return
  }

  try {
    isLoading.value = true
    const response = await axios.post(API_URL, {
      body: questionText
    })
    answer.value = response.data
  } catch (error) {
    console.error('Error:', error)
    alert('Failed to send question. Please try again.')
  } finally {
    isLoading.value = false
  }
}

function clear() {
  question.value = ''
  answer.value = ''
}
</script>

<template>
  <header>
    <div>
      <h1>Ask something about the project</h1>
      <textarea v-model="question" placeholder="Type your question here..." rows="4"></textarea>
      <br/>
      <button id="ask-button" @click="ask()" :disabled="isLoading">Ask</button>
      <button id="clear-button" style="margin-left: 10px;" @click="clear()">Clear</button>
      <p style="margin-top: 10px;">{{ answer }}</p>
    </div>
  </header>
</template>

<style scoped>
header {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  margin: 0;
  padding: 0;
}

div {
  text-align: center;
}

h1 {
  margin: 0;
  padding: 0;
}

textarea {
  width: 80%;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f8f9fa;
}

button {
  padding: 10px 20px;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

#ask-button {
  background-color: #4CAF50;
}

#ask-button:hover {
  background-color: #45a049;
}

#clear-button {
  background-color: #1c84d9;
}

#clear-button:hover {
  background-color: #1976D2;
}
</style>
