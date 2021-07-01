<template>
    <div>
        <h1>
            DOCTOR LIST
        </h1>
        <input type="text" v-model="keyword" @input="getresults" placeholder="SEARCH DATA"/>
        <p>Results are :</p>
        <div>
            <center>
            <table border="1px">
                <tr>
                <td><em>Name</em></td>
                <td><em>Specialisation</em></td>
                <td><em>Place</em></td>
                <td><em>State</em></td>
                </tr>
                <tr v-for="item in list" v-bind:key="item.id">
                <td>{{item.name}}</td>
                <td>{{item.specification}}</td>
                <td>{{item.place}}</td>
                <td>{{item.state}}</td>
                </tr>
            </table>
            </center>
        </div>    
    </div>
</template>
<script>
import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios';
Vue.use(VueAxios,axios)
export default{
        name:"doctorlist",
        data(){
            return{
                keyword:'',
                list : [],
            }
        },
        watch:{
            keyword:function(val){
                if(val.length > 3){
                    this.getresults();
                }
            }
        },
        methods :    //instead of method
        {
            getresults(){
                Vue.axios.get('http://127.0.0.1:8000/doctor/?search='+this.keyword)
                .then(resp=>{
                        this.list=resp.data
                        console.log(resp)
                })}
        },
//        created(){
//            this.getresults()
//        }
}
</script>

