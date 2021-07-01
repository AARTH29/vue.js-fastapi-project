<template>
    <div>
        <h1>
            DOCTOR LIST
        </h1>
        <input type="text" v-model="keyword"  placeholder="SEARCH DATA"/>
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
                <tr v-for="item in doctorsfilter" v-bind:key="item.id">
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

export default({
        name:"dlist",
        data(){
            return{
                keyword:'',
                list : [],
            }
        },
        
        watch:{
            list:{
                handler(){
                    localStorage.setItem('keyword',JSON.stringify(this.list))
                },
                deep: true
            }
        },
        mounted(){
            if(localStorage.getItem("list")){
                this.list = JSON.parse(localStorage.getItem("list"))
            }
            else{
            axios.get('http://127.0.0.1:8000/doctor/?search='+this.keyword)
            .then(response =>{
                this.list = response.data
                console.log(response)
            })
            .catch(error=>{
                console.log(error)
            }) }
        },
        computed:
        {
            doctorsfilter(){
                const val = this.keyword.toLowerCase()
                return this.list.filter(list=>{
                    let byname = list.name.toLowerCase().indexOf(val)!== -1 ;
                    let byspecification = list.specification.toLowerCase().indexOf(val)!== -1;
                    let byplace = list.place.toLowerCase().indexOf(val)!== -1;
                    let bystate = list.state.toLowerCase().indexOf(val)!== -1;
                    if(byname == true){
                        return byname;
                    }
                    else if(byspecification == true){
                        return byspecification;
                    }
                    else if(byplace == true){
                        return byplace;
                    }
                    else{
                        return bystate;
                    }
                })
            }
        }
})
</script>

