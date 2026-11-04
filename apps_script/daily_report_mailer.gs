/**
 * BlueStone SEO daily report mailer (Google Apps Script, runs in Google's cloud as the owner).
 *
 * dispatchReport: a daily 10 AM IST trigger starts the GitHub workflow.
 * doPost: the workflow posts the finished report here and it is sent from the owner's Gmail.
 *
 * Script properties (Project Settings -> Script properties):
 *   RECIPIENTS    comma-separated addresses
 *   SHARED_TOKEN  same value as the APPS_SCRIPT_TOKEN GitHub secret
 *   GITHUB_PAT    fine-grained token for this repo with Actions: read and write
 */
const REPO = 'KingVikasIndoria/bluestone-seo-handoff';
const WORKFLOW = 'daily_seo_dashboard_sync.yml';
const TZ = 'Asia/Kolkata';
const props = PropertiesService.getScriptProperties();

function dispatchReport() {
  const url = 'https://api.github.com/repos/' + REPO + '/actions/workflows/' + WORKFLOW + '/dispatches';
  UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    headers: {
      Authorization: 'Bearer ' + props.getProperty('GITHUB_PAT'),
      Accept: 'application/vnd.github+json'
    },
    payload: JSON.stringify({ ref: 'main' })
  });
}

function reply_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const body = JSON.parse(e.postData.contents);
  if (body.token !== props.getProperty('SHARED_TOKEN')) {
    return reply_({ ok: false, error: 'bad token' });
  }
  // The GitHub cron can also fire later in the day: only the first report of the day is sent.
  const today = Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd');
  if (props.getProperty('LAST_SENT') === today) {
    return reply_({ ok: true, skipped: 'already sent today' });
  }
  GmailApp.sendEmail(props.getProperty('RECIPIENTS'), body.subject, body.text, {
    htmlBody: body.html,
    name: 'BlueStone SEO Bot'
  });
  props.setProperty('LAST_SENT', today);
  return reply_({ ok: true });
}

// Run once by hand to create the daily trigger (fires between about 10:05 and 10:35 AM IST).
function installTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('dispatchReport').timeBased().everyDays(1).atHour(10).nearMinute(20).inTimezone(TZ).create();
}

// Run by hand between tests, so another test report can go out the same day.
function clearLastSent() {
  props.deleteProperty('LAST_SENT');
}
