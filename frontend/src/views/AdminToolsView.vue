<template>
    <div class="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-3xl mx-auto">
        <h1 class="text-3xl font-bold text-gray-900 text-center mb-8">Study Tools</h1>
        
        <div class="bg-white shadow-md rounded-lg overflow-hidden">
          <div class="flex border-b border-gray-200">
            <button
              v-for="tool in tools"
              :key="tool.id"
              @click="activeTool = tool.id"
              :class="[
                'flex-1 text-center py-4 px-4 text-sm font-medium focus:outline-none',
                activeTool === tool.id
                  ? 'text-purple-600 border-b-2 border-purple-600'
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              {{ tool.name }}
            </button>
          </div>
          
          <div class="p-6">
            <!-- Generate Questions Form -->
            <form v-if="activeTool === 'generate'" @submit.prevent="handleGenerateQuestions" class="space-y-4">
              <div>
                <label for="use-default-prompt" class="block text-sm font-medium text-gray-700">Use sample prompt </label>
                <input
                  type="checkbox"
                  id="use-default-prompt"
                  v-model="generateQuestions.useDefaultPrompt"
                  @change="setDefaultPrompt"
                  class="mt-1 block">
              </div>

              <div v-if="generateQuestions.useDefaultPrompt">
                <!-- <label for="item" class="block text-sm font-medium text-gray-700">Generate Questions about: (Comma separated list of all items you want to generate data for. Note: each takes about 20 seconds)</label>
                <input type="text" id="prompt" v-model="generateQuestions.prompt" rows="12" cols="90" class="large-textarea mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 sm:text-sm" required> -->
                <!-- <input
                  type="text"
                  id="item"
                  v-model="generateQuestions.item"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
                  placeholder="Enter item..."
                > -->
                <!-- <label for="defaultPrompt" class="block text-sm font-medium text-gray-700">Prompt</label>
                <textarea id="defaultPrompt" v-model="generateQuestions.prompt" rows="12" cols="90" class="large-textarea mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 sm:text-sm" required></textarea> -->
                
              </div>
              <div>
                <label for="prompt" class="block text-sm font-medium text-gray-700">Prompt</label>
                <textarea type="text" id="prompt" v-model="generateQuestions.prompt" rows="12" cols="90" class="large-textarea mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 sm:text-sm" required></textarea>
              </div>
              <div>
                <label for="modelType" class="block text-sm font-medium text-gray-700">Model</label>
                <select id="modelType" v-model="generateQuestions.model" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm rounded-md">
                  <option value="gpt-4">GPT 4</option>
                  <option value="gpt-4-mini"> GPT 4 mini</option>
                  <option value="gpt-3"> GPT 3</option>
                </select>      
              </div>
              <div>
                <label for="download-file-type" class="block text-sm font-medium text-gray-700">Download response as</label>
                <select id="download-file-type" v-model="generateQuestions.downloadTypes" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm rounded-md">
                  <option value="json">JSON</option>
                  <option value="excel"> Excel</option>
                  <option value="word"> Word File</option>
                </select>      
              </div>
              <div>
                  <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                    <div class="space-y-1 text-center">
                      <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                      </svg>
                      <div class="flex text-sm text-gray-600">
                        <label for="file-import" class="relative cursor-pointer bg-white rounded-md font-medium text-purple-600 hover:text-purple-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-purple-500">
                          <span>Upload files</span>
                          <input id="file-import" name="file-import" type="file" class="sr-only" @change="handleFileChange">
                        </label>
                        <p class="pl-1">or drag and drop</p>
                      </div>
                      <p class="text-xs text-gray-500">
                       File type: {{ importExport.fileType }}
                      </p>
                    </div>
                  </div>
              </div>
              <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                Generate Questions
              </button>
            </form>
              <div v-if="isProcessing"> Please wait. . . This may take up to {{countdown}} seconds. </div>
              <div>
                <div v-if="responseData" class="mt-4 p-4 bg-gray-100 rounded-lg shadow">
                  <h3 class="text-lg font-semibold text-gray-800">Response Data</h3>
                  <!-- Action buttons: Copy and Download -->
                  <div>
                    <!-- Copy to clipboard button -->
                    <button @click="copyToClipboard" class="text-purple-500 hover:text-purple-700 mr-4">
                      <i class="pi pi-copy"></i> Copy
                    </button>

                    <!-- Download as file button -->
                    <button @click="downloadAsFile" class="text-purple-500 hover:text-purple-700">
                      <i class="pi pi-download"></i> Download
                    </button>
                  </div>
                  <pre class="whitespace-pre-wrap text-sm text-gray-600">{{ formattedResponse }}</pre>
                </div>
              </div>

              
            
  
            <!-- Web Scraper Form -->
            <form v-if="activeTool === 'scraper'" @submit.prevent="handleWebScraper" class="space-y-4">
              <div>
                <label for="site" class="block text-sm font-medium text-gray-700">Site URL</label>
                <input type="url" id="site" v-model="webScraper.site" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 sm:text-sm" required>
              </div>
              <div>
                <label for="content" class="block text-sm font-medium text-gray-700">HTML Tags to Scrape</label>
                <input type="text" id="content" v-model="webScraper.content" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 sm:text-sm" placeholder="e.g. p, h1, .class-name" required>
              </div>
              <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                Start Scraping
              </button>
            </form>
  
            <!-- Upload to AWS Form -->
            <form v-if="activeTool === 'aws'" @submit.prevent="handleAWSUpload" class="space-y-4">
              <div>
                <label for="bucketName" class="block text-sm font-medium text-gray-700">Bucket Name</label>
                <input type="text" id="bucketName" v-model="awsUpload.bucketName" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 sm:text-sm" required>
              </div>
              <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                <div class="space-y-1 text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                  <div class="flex text-sm text-gray-600">
                    <label for="file-upload" class="relative cursor-pointer bg-white rounded-md font-medium text-purple-600 hover:text-purple-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-purple-500">
                      <span>Upload a file</span>
                      <input id="file-upload" name="file-upload" type="file" class="sr-only" @change="handleFileChange">
                    </label>
                    <p class="pl-1">or drag and drop</p>
                  </div>
                  <p class="text-xs text-gray-500">
                    PNG, JPG, GIF up to 10MB
                  </p>
                </div>
              </div>
              <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                Upload to AWS
              </button>
            </form>
  
            <!-- Import/Export Form -->
            <form v-if="activeTool === 'importexport'" @submit.prevent="handleImportExport" class="space-y-4">
              <div>
                <label for="fileType" class="block text-sm font-medium text-gray-700">File Type</label>
                <select id="fileType" v-model="importExport.fileType" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm rounded-md">
                  <option value="pdf">.pdf</option>
                  <option value="json">.json</option>
                  <option value="csv">.csv</option>
                </select>
              </div>
              <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                <div class="space-y-1 text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                  <div class="flex text-sm text-gray-600">
                    <label for="file-import" class="relative cursor-pointer bg-white rounded-md font-medium text-purple-600 hover:text-purple-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-purple-500">
                      <span>Upload a file</span>
                      <input id="file-import" name="file-import" type="file" class="sr-only" @change="handleFileChange">
                    </label>
                    <p class="pl-1">or drag and drop</p>
                  </div>
                  <p class="text-xs text-gray-500">
                    File type: {{ importExport.fileType }}
                  </p>
                </div>
              </div>
              <div class="flex space-x-4">
                <button type="button" @click="handleImport" class="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                  Import
                </button>
                <button type="button" @click="handleExport" class="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                  Export
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import axios from 'axios';
  import { API_URL } from '@/utils/constants';
  import {useToast} from 'vue-toastification';

  const toast = useToast();
  const tools = [
    { id: 'generate', name: 'Generate Questions' },
    { id: 'scraper', name: 'Web Scraper' },
    { id: 'aws', name: 'Upload to AWS' },
    { id: 'importexport', name: 'Import/Export' },
  ]
  
  const activeTool = ref('generate')
  
  const defaultPrompt =
    `Generate exactly 10 questions about {{ item }} in strict JSON format. Each question should have the following structure:
    {
      "question": "The question text",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "correct_answer": "The correct option",
      "explanation": "Explanation of why the correct answer is right"
    }
    The output should only be valid JSON. Do not include any text or comments outside the JSON structure. do not prefix with the word 'JSON'. your response should only be an array of JSONs.`

  
  const generateQuestions = ref({
    useDefaultPrompt: false,
    defaultPrompt: defaultPrompt,
    prompt: '',
    model: 'gpt-4',
    item: '',
    downloadTypes: 'json'
  })
  
  const countdown = ref(30);  
  let intervalId = null; 
  // const firstItem = computed( () => {
  //   generateQuestions.value.item.split(',')[0].trim();
  // } )
  const setDefaultPrompt = () => {
      if (generateQuestions.value.useDefaultPrompt) {
        generateQuestions.value.prompt = defaultPrompt
      }
      else{
        generateQuestions.value.prompt = ''
      }
    }
  
  const startCountdown = () => {
    countdown.value = 30;
    intervalId = setInterval(() => {
      if (countdown.value > 0) {
        countdown.value -= 1;
      } else {
        clearInterval(intervalId);
      }
    }, 1000);
  };

  const webScraper = ref({
    site: '',
    content: '',
  })
  
  const awsUpload = ref({
    bucketName: '',
    file: null,
  })
  
  const importExport = ref({
    fileType: 'pdf',
    file: null,
  })
  
  const responseData = ref(null);
  const isProcessing = ref(false)

  const formattedResponse = computed(() => JSON.stringify(responseData.value, null, 2))

  const handleGenerateQuestions = async () => {
    isProcessing.value = true
    startCountdown()
    // const itemArray = generateQuestions.value.item.split(',').map(item => item.trim());
    try{
      const promptResponse = await axios.post(`${API_URL}/ai/process_prompt/`, {
          // use_default: generateQuestions.value.useDefaultPrompt,
          // items: generateQuestions.value.useDefaultPrompt ? itemArray : [],
          prompt: generateQuestions.value.prompt,
          model: generateQuestions.value.model,
        }, 
        );
        // let rawResponse = JSON.stringify(promptResponse.data.data)
        toast.success('Data Generated Successfully')
        responseData.value = promptResponse.data.data //rawResponse.replace(/\n/g, '')
        isProcessing.value = false //
      
    }
    catch (error) {
      toast.error('Something went wrong. Please try again')
      console.error('Error handling response:', error);
      isProcessing.value = false
    }
    

    // Implement question generation logic here
  }

  
  const copyToClipboard = () => {
      const jsonString = JSON.stringify(responseData.value, null, 2);
      navigator.clipboard.writeText(jsonString)
        .then(() => {
          // alert("Copied to clipboard!");
          toast.success("Copied to clipboard")
        })
        .catch((error) => {
          toast.error("Failed to copy:", error);
        });
    };

    // Function to download the JSON data as a file
    const downloadAsFile = () => {
      const jsonString = JSON.stringify(responseData.value, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'response.json';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };

  
  const handleWebScraper = () => {
    console.log('Web scraping:', webScraper.value)
    // Implement web scraping logic here
  }
  
  const handleAWSUpload = () => {
    console.log('Uploading to AWS:', awsUpload.value)
    // Implement AWS upload logic here
  }
  
  const handleImportExport = () => {
    console.log('Import/Export:', importExport.value)
    // Implement import/export logic here
  }
  
  const handleFileChange = (event) => {
    const file = event.target.files[0]
    if (activeTool.value === 'aws') {
      awsUpload.value.file = file
    } else if (activeTool.value === 'importexport') {
      importExport.value.file = file
    }
  }
  
  const handleImport = () => {
    console.log('Importing file:', importExport.value)
    // Implement import logic here
  }
  
  const handleExport = () => {
    console.log('Exporting file:', importExport.value)
    // Implement export logic here
  }

  // onMounted( 
  //   // async () => {
  //   //   try {
  //   //     const response = await axios.get(`${API_URL}/ai/download_prompt/`); // Replace with your API URL
  //   //     data.value = response.data;
  //   //   } catch (err) {
  //   //     console.log(err || 'Failed to load data');
  //   //   }
  //   // }
  //   )
  </script>
  
  <style scoped>
  /* Add any additional component-specific styles here */
  .large-textarea {
    width: 100%; /* Makes it take up the full width of the parent container */
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  </style>