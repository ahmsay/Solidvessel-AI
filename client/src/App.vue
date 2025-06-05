<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const question = ref('')
const answer = ref('')

const API_URL = 'https://kw5uzneejhbujvqypkrcsi4wji0dodqu.lambda-url.eu-central-1.on.aws/'

function ask() {
  const questionText = question.value.trim()
  
  if (!questionText) {
    alert('Please enter a question')
    return
  }

  try {
    console.log('Sending question:', questionText)
      axios.post(API_URL, {
      body: questionText
    })
    .then(response => {
      console.log('Response:', response.data)
      answer.value = response.data
    })
    .catch(error => {
      console.error('Error:', error)
      alert('Failed to send question. Please try again.')
    })
  } catch (error) {
    console.error('Error:', error)
    alert('Failed to send question. Please try again.')
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
      <button @click="ask()">Ask</button>
      <button style="margin-left: 10px;" @click="clear()">Clear</button>
      <p>{{ answer }}</p>
    </div>
  </header>
</template>

<style scoped>
header {
  display: flex;
  justify-content: center;
  width: 100%;
  margin: 0;
  padding: 0;
}

div {
  text-align: center;
  margin: 0;
  padding: 0;
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
}

button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
