/**
 * BlueStone SEO daily report mailer (Google Apps Script, runs in Google's cloud as the owner).
 *
 * sendDailyReport starts the GitHub workflow, waits for the report it produces,
 * sends it from the owner's Gmail, then deletes the report file from GitHub.
 *
 * Script properties (Project Settings -> Script properties):
 *   RECIPIENTS  comma-separated addresses
 *   GITHUB_PAT  fine-grained token for this repo with Actions: read and write
 */
const REPO = 'KingVikasIndoria/bluestone-seo-handoff';
const WORKFLOW = 'daily_seo_dashboard_sync.yml';
const ARTIFACT = 'daily-report';
const API = 'https://api.github.com/repos/' + REPO + '/actions/';
const TZ = 'Asia/Kolkata';
const MAX_WAIT_MS = 5 * 60 * 1000;  // Apps Script stops a run at 6 minutes
const props = PropertiesService.getScriptProperties();

function github_(path, options) {
  const opts = Object.assign({
    headers: {
      Authorization: 'Bearer ' + props.getProperty('GITHUB_PAT'),
      Accept: 'application/vnd.github+json'
    }
  }, options || {});
  return UrlFetchApp.fetch(path.indexOf('http') === 0 ? path : API + path, opts);
}

function waitForArtifact_(startedAt) {
  const deadline = Date.now() + MAX_WAIT_MS;
  while (Date.now() < deadline) {
    Utilities.sleep(20000);
    const found = JSON.parse(github_('artifacts?per_page=5&name=' + ARTIFACT).getContentText()).artifacts
      .filter(function (a) { return !a.expired && new Date(a.created_at).getTime() >= startedAt; });
    if (found.length) return found[0];
  }
  throw new Error('No report from GitHub after 5 minutes. Check the Actions tab of ' + REPO);
}

function sendDailyReport() {
  const startedAt = Date.now() - 60000;
  github_('workflows/' + WORKFLOW + '/dispatches', {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ ref: 'main' })
  });
  const artifact = waitForArtifact_(startedAt);

  // GitHub redirects to a signed storage URL, which must be fetched without the token.
  const redirect = github_(artifact.archive_download_url, { followRedirects: false });
  const zip = UrlFetchApp.fetch(redirect.getHeaders().Location).getBlob().setContentType('application/zip');
  const report = JSON.parse(Utilities.unzip(zip)[0].getDataAsString('UTF-8'));

  GmailApp.sendEmail(props.getProperty('RECIPIENTS'), report.subject, report.text, {
    htmlBody: report.html,
    name: 'BlueStone SEO Bot'
  });
  github_('artifacts/' + artifact.id, { method: 'delete' });
}

// Run once by hand to create the daily trigger (starts between about 10:05 and 10:35 AM IST).
function installTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('sendDailyReport').timeBased().everyDays(1).atHour(10).nearMinute(20).inTimezone(TZ).create();
}
