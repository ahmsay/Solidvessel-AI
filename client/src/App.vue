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
  <v-app style="background: linear-gradient(135deg, #456aaf, #d4d0d0);">
    <v-main>
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-row justify="center">
              <v-card>
                <template v-slot:title>
                  <span class="font-weight-black">Ask something about the project</span>
                </template>
                <v-card-text>
                  <v-textarea v-model="question" label="Type your question here..." rows="4"></v-textarea>
                </v-card-text>
                <v-card-text>
                  <div class="d-flex justify-center">
                    <v-btn color="primary" @click="ask()" :disabled="isLoading">Ask</v-btn>
                    <v-btn color="secondary" class="ml-3" @click="clear()">Clear</v-btn>
                  </div>
                </v-card-text>
              </v-card>
              <p class="mt-5">{{ answer }}</p>
            </v-row>
          </v-col>
        </v-row>
    </v-container>
    </v-main>
  </v-app>
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
</style>
