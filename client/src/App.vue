<script setup lang="ts">
import { ref } from 'vue'
import axios, { AxiosError } from 'axios'

const question = ref('')
const answer = ref('')
const previousQuestion = ref('')
const isLoading = ref(false)

const API_URL = 'https://kw5uzneejhbujvqypkrcsi4wji0dodqu.lambda-url.eu-central-1.on.aws/'

async function ask() {
  const questionText = question.value.trim()

  if (!questionText) {
    return
  }

  previousQuestion.value = questionText
  clearForNextConversation()

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

function clearForNextConversation() {
  question.value = ''
  answer.value = ''
}

function goToSource() {
  window.open('https://github.com/ahmsay/Solidvessel-AI', '_blank')
}
</script>

<template>
  <v-app class="bg-gradient">
    <v-main>
      <v-container class="fill-height d-flex align-center">
        <v-row justify="center">
          <v-col cols="12" md="6" sm="8">
            <v-card color="rgba(58, 95, 166, 0.2)" class="px-sm-6 py-sm-6" prepend-icon="mdi-message-text" elevation="12">
              <template v-slot:title>
                <span class="text-h5" style="white-space: normal; word-wrap: break-word;">Ask something about the project</span>
              </template>
              <v-card-text>
                <v-textarea v-model="question" label="Type your question here..." rows="4" @keyup.enter="ask()"></v-textarea>
              </v-card-text>
              <v-card-text class="pt-0">
                <div v-if="previousQuestion" class="text-end">
                  <p class="custom-chip">{{ previousQuestion }}</p>
                </div>
                <div v-if="answer" class="text-start mt-3">
                  <p class="custom-chip">{{ answer }}</p>
                </div>
              </v-card-text>
            </v-card>
            <v-footer color="transparent" class="d-flex justify-center">
              <v-btn class="mt-2" variant="text" icon @click="goToSource">
                <v-icon size="x-large">mdi-github</v-icon>
              </v-btn>
            </v-footer>
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

.custom-chip {
    display: inline-block;
    min-width: auto;
    padding: 8px 16px;
    border-radius: 20px;
    background-color: rgba(80, 117, 187, 0.3);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.bg-gradient {
    background: linear-gradient(135deg, #456aaf, #d4d0d0);
}
</style>
