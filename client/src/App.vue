<script setup lang="ts">
import { ref } from 'vue'

const question = ref('')

function send() {
  console.log('Sending question:', question.value)
  question.value = ''
}
</script>

<template>
  <header>
    <div>
      <h1>Ask something about the project</h1>
      <textarea v-model="question" placeholder="Type your question here..." rows="4"></textarea>
      <br/>
      <button @click="send()">Ask</button>
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
