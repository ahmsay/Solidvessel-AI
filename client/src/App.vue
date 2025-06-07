<script setup lang="ts">
import { ref } from 'vue'
import axios, { AxiosError } from 'axios'

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
    const errorMessage = (error as AxiosError).response?.status === 403 
      ? 'You are not authorized.'
      : 'Failed to send question. Please try again.'
    alert(errorMessage)
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
      <span class="text-h4">Ask something about the project</span>
      <v-textarea v-model="question" label="Type your question here..." rows="4"></v-textarea>
      <v-btn color="primary" @click="ask()" :disabled="isLoading">Ask</v-btn>
      <v-btn color="secondary" class="ml-3" @click="clear()">Clear</v-btn>
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
</style>
