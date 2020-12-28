<template>
<div>
  {{ loading }}
  <div v-for="item in items" v-if="filterData(item)" >
    {{ item.country }}: {{ item.rate_14_day }} {{ item.year_week }}
  </div>
</div>

</template>

<script>
import coronaData from "../assets/ECDC.json";

export default {
  name: 'Main',
  data() {
    return {
      loading: false,
      items: {},
      lastYearWeek: {}
    }
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData(){
      this.items = coronaData;
    },
    filterData(item){
     return (item.country_code === 'POL' || item.country_code === 'UKR') && item.year_week === '2020-51' && item.indicator==='cases'
    },
    getWeekNumber(d) {
      // Copy date so don't modify original
      d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
      // Set to nearest Thursday: current date + 4 - current day number
      // Make Sunday's day number 7
      d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay()||7));
      // Get first day of year
      var yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
      // Calculate full weeks to nearest Thursday
      var weekNo = Math.ceil(( ( (d - yearStart) / 86400000) + 1)/7);
      // Return array of year and week number
      return d.getUTCFullYear()+'-'+weekNo;
  },
  filterWeeks(item, d){
    return item.year_week === this.getWeekNumber(d)
  }
  },
}
</script>
