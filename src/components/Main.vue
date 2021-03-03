<template>
    <div>
        <b-navbar class="navClass" toggleable="lg" type="dark" variant="info">
            <b-navbar-nav>
                <b-dropdown :text="translations[locale].chooseLanguage">
                    <b-dropdown-item :href= "isFull ? '/full?lang=pl' : '/?lang=pl'">PL</b-dropdown-item>
                    <b-dropdown-item :href= "isFull ? '/full?lang=ua' : '/?lang=ua'">UA</b-dropdown-item>
                    <b-dropdown-item :href= "isFull ? '/full' : '/'">EN</b-dropdown-item>
                </b-dropdown>
                <b-nav-item>
                 <model-list-select 
                    class="selectClass"
                    v-if="isFull"
                    :list="countries"
                     v-model="chosenCountry"
                     option-text="country"
                     option-value="country"
                     :placeholder="translations[locale].selectCountryToCompare"
                     @select="filterItems()"
                    >
                </model-list-select>
                </b-nav-item>
            </b-navbar-nav>
        </b-navbar>

    <b-container fluid>
        <div>{{translations[locale].copyrightPolicy1}}<a href="https://www.ecdc.europa.eu/en/copyright" target="_blank">{{translations[locale].copyrightPolicy2}}</a>. {{translations[locale].originalSource1}}<a href="https://www.ecdc.europa.eu/en/publications-data/data-national-14-day-notification-rate-covid-19"
                target="_blank">{{translations[locale].here}}</a>.</div>
        <div>{{translations[locale].warning}} {{translations[locale].disclaimer}}</div>
        <div>{{translations[locale].currentWeek}}: <b>{{currentWeek}}</b></div>
        <div>{{translations[locale].mostRecentWeek}}: <b>{{mostRecentECDCWeek}}</b></div>
        <div>{{translations[locale].dataPublishedOn}}: <b>{{this.getDateOfWeek()}}</b></div>
        <div>{{translations[locale].mozDatePrognosis}}: <b>{{this.getDateOfWeek(true)}}</b></div>
        <div>{{ translations[locale].chooseWeek }}: 
        <select v-model="chosenWeek" name="week">
            <option v-for="week in weeks" :value="week">{{ week }}</option>
        </select>
      </div>
        <div v-if="!isFull">{{ translations[locale].seeAllCountries }} <a :href=" locale==='en' ? '/full' : '/full?lang='+ locale">{{translations[locale].here}}</a>.</div>
        <div v-else> {{ translations[locale].seePolandAndUkraine }} <a :href=" locale==='en' ? '/' : '/?lang='+ locale">{{translations[locale].here}}</a>.</div>
        <b-table 
        hover 
        small
        :items="filteredItems" 
        :fields="fields"></b-table>
    </b-container>
    </div>
</template>

<script>
import translatedData from "../assets/translations.json";
import { ModelListSelect } from 'vue-search-select';

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
                    country: ''
                },
            fields: [
                {
                    key: 'country',
                    sortable: false
                },
                {
                    key: 'rate_14_day',
                    sortable: true
                }
            ]
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
        countries() {
            let filtered = []
                this.items.forEach(item => {
                    let object = {
                        country: item.country
                    };
                if ((!filtered.some(el => el.country === object.country))) {
                    filtered.push(object);
                } 
            });
            return filtered.sort(this.compare);
        },
        filteredItems(){
            let filtered = [];
            this.items.forEach(item => {
                if ((!filtered.includes(item.country)) && this.filterData(item)) {
                    filtered.push(item);
                } 
            });
            return filtered;            
        
        },
    },
    created() {
        this.fetchData();
        this.getMostRecentECDCWeek();
        this.getWeeks();
        this.getDateOfWeek(this.mostRecentECDCWeek);
    },
    methods: {
        fetchData() {
            this.translations = translatedData
        },
        compare(a, b) {
            if ( a.country < b.country ){
                return -1;
            }
            if ( a.country > b.country ){
                return 1;
            }
            return 0;
        },
        filterData(item) {
            if (!this.chosenCountry.country){
                return item.year_week === this.chosenWeek
            } else {
                return ((item.year_week === this.chosenWeek) && (item.country==="Ukraine" || item.country === this.chosenCountry.country))
            }
            
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
        },
        getDateOfWeek(isForecast = false) {
            let week = this.mostRecentECDCWeek;
            let weekSplit = week.split('-');
            let y = parseInt(weekSplit[0]);
            let w = parseInt(weekSplit[1])+1;
            let date = new Date(y, 0, (1 + (w) * 7)); // Elle's method
            date.setDate(date.getDate() + (4 - date.getDay())); // 0 - Sunday, 1 - Monday etc
            
            let monthNumber = date.getUTCMonth(); //months from 1-12
            let day = !isForecast ? date.getUTCDate() : date.getUTCDate()+1;
            let year = date.getUTCFullYear();

            return day+1 + ' ' + this.translations[this.locale].months[monthNumber] + ' ' + year;
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

.container-fluid div {
    margin: 5px;
}

.selectClass {
    min-width: 150px !important;
    color: black !important;
}

.navClass {
    min-height: 70px;
}

</style>
