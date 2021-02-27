<template>
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-nav>
                <b-dropdown :text="translations[locale].chooseLanguage">
                    <b-dropdown-item :href= "isFull ? '/full?lang=pl' : '/?lang=pl'">PL</b-dropdown-item>
                    <b-dropdown-item :href= "isFull ? '/full?lang=ua' : '/?lang=ua'">UA</b-dropdown-item>
                    <b-dropdown-item :href= "isFull ? '/full' : '/'">EN</b-dropdown-item>
                </b-dropdown>
                <b-nav-item>
                 <model-list-select 
                    :list="filterItems(true)"
                     v-model="chosenCountry"
                     option-text="country"
                     option-value="country"
                     placeholder="select item"
                    >
                </model-list-select>
                </b-nav-item>
            </b-navbar-nav>
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
        <div v-for="item in filterItems()">
            <div class="cell">{{ item.country }}: {{ item.rate_14_day }}</div>
        </div>
    </div>
</template>

<script>
import translatedData from "../assets/translations.json";
import { ModelListSelect    } from 'vue-search-select';

export default {
    name: 'Main',
    components: {
        ModelListSelect   
    },
    data() {
        return {
            loading: false,
            lastYearWeek: {},
            weeks: [],
            mostRecentECDCWeek: null,
            currentWeek: this.getWeekNumber(new Date),
            chosenWeek: null,
            locale: this.$route.query.lang ? this.$route.query.lang : 'en',
            translations: {},
            chosenCountry: {
                country: '',
                rate_14_day: '',
                weekly_count: '',
                year_week: ''
                }
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
        },
    },
    created() {
        this.fetchData();
        this.getMostRecentECDCWeek();
        this.getWeeks();
    },
    methods: {
        adjustDateInChosenCountry(e) {
            if (this.chosenCountry.year_week !== this.chosenWeek) {
                console.log('fired');
                this.filterData().forEach(item => {
                    if ((item.country === e.country) && (item.year_week === this.chosenWeek)) {
                        this.chosenCountry = item;
                    }
                })
            }
        },
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
        filterItems(sortAlphabetically = false) {
            let filtered = [];
            this.items.forEach(item => {
                if ((!filtered.includes(item.country)) && this.filterData(item)) {
                    filtered.push(item);
                } 
            });

            if (sortAlphabetically) {
                return filtered.sort(function(a, b){
                if(a.country < b.country) { return -1; }
                if(a.country > b.country) { return 1; }
                return 0;
            });
            } else {
                return filtered;            
            }
            
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
<style scoped>
.cell {
    border: 1px solid black;
    margin-left: 2px;
    padding-left: 5px;
    width: 300px;
    border-bottom: none;
}

.multi {
    position: absolute;
    z-index: 50;
}


</style>
