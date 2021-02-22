<template>
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <div>
                {{ translations[locale].chooseLanguage }}: 
                <a :href= "isFull ? '/full?lang=pl' : '/?lang=pl'">PL </a>
                <a :href= "isFull ? '/full?lang=ua' : '/?lang=ua'">UA </a>
                <a :href= "isFull ? '/full' : '/'">EN </a>
            </div>
        </b-navbar>
        <div>{{translations[locale].copyrightPolicy1}} <a href="https://www.ecdc.europa.eu/en/copyright" target="_blank">{{translations[locale].copyrightPolicy2}} </a>. {{translations[locale].originalSource1}}<a href="https://www.ecdc.europa.eu/en/publications-data/data-national-14-day-notification-rate-covid-19"
                target="_blank">{{translations[locale].here}}</a>. </div>
        <div>{{translations[locale].warning}}</div>
        <br>
        <div>{{translations[locale].currentWeek}}: {{currentWeek}}</div>
        <div>{{translations[locale].mostRecentWeek}}: {{mostRecentECDCWeek}}</div>
        {{ translations[locale].chooseWeek }}: <select v-model="chosenWeek" name="week">
        <option v-for="week in weeks" :value="week">{{ week }}</option>
      </select>
        <div v-if="!isFull">{{ translations[locale].seeAllCountries }} <a :href=" locale==='en' ? '/full' : '/full?lang='+ locale">{{translations[locale].here}}</a>.</div>
        <div v-else> {{ translations[locale].seePolandAndUkraine }} <a :href=" locale==='en' ? '/' : '/?lang='+ locale">{{translations[locale].here}}</a>.</div>
        <div v-for="item in items" v-if="filterData(item)">
            <div>{{ item.country }}: {{ item.rate_14_day }}</div>
        </div>
    </div>
</template>

<script>
import translatedData from "../assets/translations.json";

export default {
    name: 'Main',
    data() {
        return {
            loading: false,
            lastYearWeek: {},
            weeks: [],
            mostRecentECDCWeek: null,
            currentWeek: this.getWeekNumber(new Date),
            chosenWeek: null,
            locale: this.$route.query.lang ? this.$route.query.lang : 'en',
            translations: {}
        }
    },
    computed: {
        isFull() {
            return this.$route.path === '/full' ? true : false;
        },
        items() {
            if (this.isFull) {
                return require("../assets/ECDC-full.json");
            } else {
                return require("../assets/ECDC-short.json");
            }
        }
    },
    created() {
        this.fetchData();
        this.getMostRecentECDCWeek();
        this.getWeeks();
    },
    methods: {
        fetchData() {
            this.translations = translatedData
        },
        filterData(item) {
            return item.year_week === this.chosenWeek
        },
        getWeekNumber(d) {
            // Copy date so don't modify original
            d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
            // Set to nearest Thursday: current date + 4 - current day number
            // Make Sunday's day number 7
            d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
            // Get first day of year
            var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
            // Calculate full weeks to nearest Thursday
            var weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
            weekNo = weekNo.toString();
            if (weekNo.length === 1) {
                weekNo = '0' + weekNo;
            }
            // Return array of year and week number
            return d.getUTCFullYear() + '-' + weekNo;
        },
        addTrailingZeroToWeeks(week) {
            week = week.toString();
            if (week.length === 1) {
                week = '0' + week;
            }
            return week;
        },
        getWeeks() {
            let param1 = parseInt(new Date().getUTCFullYear(), 10) == parseInt(this.mostRecentECDCWeek.substring(0, 4)) ?
                parseInt(new Date().getUTCFullYear(), 10) :
                parseInt(this.mostRecentECDCWeek.substring(0, 4));
            let param2 = parseInt(new Date().getUTCFullYear(), 10) == parseInt(this.mostRecentECDCWeek.substring(0, 4)) ?
                parseInt(this.mostRecentECDCWeek.substring(5)) + 1 :
                53 + 1;

            for (let i = 2020; i < param1 + 1; i++) {
                if (i === 2020) {
                    for (let j = 51; j < 54; j++) {
                        j = this.addTrailingZeroToWeeks(j);
                        this.weeks.push(i + '-' + j);
                    }
                } else {
                    for (let j = 1; j < param2; j++) {
                        j = this.addTrailingZeroToWeeks(j);
                        this.weeks.push(i + '-' + j);
                    }
                }
            }
            this.weeks = this.weeks.reverse();
        },
        filterWeeks(item, d) {
            return item.year_week === this.getWeekNumber(d)
        },
        getMostRecentECDCWeek() {
            this.mostRecentECDCWeek = this.items[this.items.length - 1].year_week;
            this.chosenWeek = this.items[this.items.length - 1].year_week;
        }
    },
}
</script>
