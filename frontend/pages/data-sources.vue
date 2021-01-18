<template>
  <div class="container scroll">
    <div class="info-wrapper limit-width">
      <div class="close">
        <a href="#" @click.prevent="$router.push('/')"
          ><img src="~/assets/images/close-icon.svg" alt="Close"
        /></a>
      </div>
      <div class="info shadow">
        <h1>Data sources</h1>
        <h2>COVID-19 Death Count</h2>
        <p>
          We use the
          <a href="https://about-corona.net/" target="_blank"
            >About-Corona.Net</a
          >
          API to collect and display the total number of people who have sadly
          passed in each country, as a result of COVID-19.
        </p>
        <p>
          The data we receive via the
          <a href="https://about-corona.net/" target="_blank"
            >About-Corona.Net</a
          >
          API, originates from the following sources:
        </p>
        <ul class="list">
          <li>
            <a
              href="https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"
              target="_blank"
              >WHO Situation Reports</a
            >
          </li>
          <li>
            <a href="https://github.com/CSSEGISandData/COVID-19" target="_blank"
              >Data Repository by Johns Hopkins CSSE</a
            >
          </li>
          <li>
            <a
              href="http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
              target="_blank"
              >National Health Commission of the People’s Republic of China
              (NHC)</a
            >
          </li>
          <li>
            <a
              href="https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases"
              target="_blank"
              >European Centre for Disease Prevention and Control (ECDC)</a
            >
          </li>
          <li>
            <a
              href="https://www.cdc.gov/coronavirus/2019-ncov/index.html"
              target="_blank"
              >US CDC</a
            >
          </li>
          <li>
            <a
              href="http://weekly.chinacdc.cn/news/TrackingtheEpidemic.htm"
              target="_blank"
              >China CDC (CCDC)</a
            >
          </li>
          <li>
            <a href="http://dxy.cn/" target="_blank">DXY.cn.</a>
            <a href="http://3g.dxy.cn/newh5/view/pneumonia" target="_blank"
              >Pneumonia. 2020</a
            >
          </li>
        </ul>
        <p>
          Therefore, the total number of deaths we display on the Memorial when
          you first load the page, is the most recent figure compiled from these
          sources. This is updated daily.
        </p>
        <p>
          To provide a visual reminder of the ongoing situation, the number of
          deaths we display slowly increases. This incremental rise is based on
          the current rate of deaths, calculated from the last two days of data
          from the API. It is displayed for illustrative purposes only and is
          not representative of the exact times people have passed.
        </p>
        <p>
          Please do not rely on The COVID Memorial for accurate updates on the
          death counts. We are not an official source.
        </p>
        <h2>Individual Memorials</h2>
        <p>
          We have made this memorial available to everyone and we encourage you
          to include the stories of people who have died as either a direct or
          indirect result of COVID-19. Therefore, the actual number of
          individual memorials on this site may exceed the official death count
          figure, which only accounts for direct deaths.
        </p>
        <p>
          Indirect deaths are those that have occured because of the wider
          issues the pandemic has created, such as restricting access to vital
          healthcare, diversion of vital resources and a reduction in global
          aid.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  transition: {
    name: 'fade-slow',
    mode: '',
  },
}
</script>

<style lang="scss" scoped></style>
