<template>
<div>
  <select v-model="chosenWeek" name="week">
    <option v-for="week in weeks" :value="week">{{ week }}</option>
  </select>
  <div v-for="item in items" v-if="filterData(item)">
    {{ item.country }}: {{ item.rate_14_day }}
  </div>
</div>

</template>

<script>
import coronaData from "../assets/pobrane.json";

export default {
  name: 'Full',
  data() {
    return {
      loading: false,
      items: {},
      lastYearWeek: {},
      weeks: [],
      chosenWeek: null
    }
  },
  created() {
    this.fetchData();
    this.getWeeks();
  },
  methods: {
    fetchData() {
      this.items = coronaData;
    },
    test(){
      console.log('changed');
    },
    filterData(item) {
     return item.year_week === this.chosenWeek && item.indicator==='cases'
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
    getWeeks() {
      for (let i = 2020; i < 2022; i++) {
          for (let j = i === 2020 ? 51 : 1; j < 54; j++) {
          this.weeks.push(i+'-'+j);
        }
      }
    },
    filterWeeks(item, d) {
      return item.year_week === this.getWeekNumber(d)
    }
  },
}
</script>
