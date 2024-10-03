<script setup>
import {ref, defineProps} from 'vue';
import ItemList from './ItemList.vue';

defineProps({
    limit: Number,
    showButton: {
        type: Boolean,
        default: false
    }
})

const items = ref([{title: 'funny', id: 0, description: 'Lorem Ipsum dolo remit upsum cana', location: 'NY'}, {title: 'happy', id: 1, description: 'Lorem Ipsum dolo remit upsum cana Lorem Ipsum dolo remit upsum cana', location: 'NY'}, {title: 'awesome', id: 2, description: 'Lorem Ipsum dolo remit upsum Ipsum dolo remit upsum cana Lorem Ipsum dolo remit cana Lorem Ipsum dolo remit upsum cana', location: 'NY'}])
</script>

<template>
    <section class="bg-blue-50 px-4 py-10">
        <div class="container-xl lg:container m-auto">
            <h2 class="text-3xl font-bold text-green-500 mb-6 text-center">
                Items List
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <ItemList v-for="item in items.slice(0, limit || items.length)" :key="item.id" :item="item"/>
                
            </div>
            
        </div>
    </section>
    <section v-if="showButton" class="m-auto max-w-lg my-10 px-6">
      <a
        href="/jobs"
        class="block bg-black text-white text-center py-4 px-6 rounded-xl hover:bg-gray-700"
        >View All Items</a
      >
    </section>
    
</template>