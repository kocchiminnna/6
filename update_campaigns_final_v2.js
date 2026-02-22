const fs = require('fs');

const userTweets = [
  { clinicName: "エートップ美容整形外科", handle: "@atopseikei", procedure: "3月東京相談会 (3/28-29)", id: "2024794799346422139", url: "https://twitter.com/atopseikei/status/2024794799346422139" },
  { clinicName: "JAYJUN美容外科", handle: "@jayjun_jpn", procedure: "2月&3月プレミアムイベント (リフト等)", id: "2025426824977907777", url: "https://twitter.com/jayjun_jpn/status/2025426824977907777" },
  { clinicName: "フレッシュホンドクター整形外科", handle: "@freshps5512", procedure: "印象アップデート (脂肪移植・吸引)", id: "2013763475869421865", url: "https://twitter.com/freshps5512/status/2013763475869421865" },
  { clinicName: "バイウォンクリニック", handle: "@BywonClinic", procedure: "3月東京相談会 (3/28-29)", id: "2010644106146701623", url: "https://twitter.com/BywonClinic/status/2010644106146701623" },
  { clinicName: "ジャスト美容整形外科", handle: "@justprsjp", procedure: "春のイベント (デュアルピーチリフト等)", id: "2025132437538291830", url: "https://twitter.com/justprsjp/status/2025132437538291830" },
  { clinicName: "ナビ美容外科", handle: "@NAVI_KOREA_", procedure: "脂肪注入豊胸", id: "2024725191524569528", url: "https://twitter.com/NAVI_KOREA_/status/2024725191524569528" },
  { clinicName: "NANA美容外科", handle: "@nanahospital", procedure: "3月限定シークレット鼻整形イベント", id: "2024655583711023512", url: "https://twitter.com/nanahospital/status/2024655583711023512" },
  { clinicName: "ビューティーライン整形外科", handle: "@beautylinejp", procedure: "キム院長顔の脂肪吸引", id: "2024650216507658477", url: "https://twitter.com/beautylinejp/status/2024650216507658477" },
  { clinicName: "コーヘン美容外科", handle: "@cohenclinic", procedure: "新年イベント (小鼻縮小等)", id: "2006300297220771891", url: "https://twitter.com/cohenclinic/status/2006300297220771891" },
  { clinicName: "ハイボム美容外科", handle: "@hivompsJP", procedure: "2月末迄限定 (人中手術等) & 東京相談会 (3/7-8)", id: "2024398390113767921", url: "https://twitter.com/hivompsJP/status/2024398390113767921" }
];

const content = fs.readFileSync('index.html', 'utf8');
const match = content.match(/const campaigns = \[\s*([\s\S]*?)\s*\];/);
if (!match) process.exit(1);

let campaignsRaw = match[1];
const existingCampaigns = [];
const regex = /{[\s\S]*?}/g;
let m;
while ((m = regex.exec(campaignsRaw)) !== null) {
    const raw = m[0];
    const clinicName = (raw.match(/clinicName:\s*"(.*?)"/) || [])[1];
    const id = (raw.match(/id:\s*"(.*?)"/) || (raw.match(/tweetId:\s*"(.*?)"/) || []))[1];
    const handle = (raw.match(/handle:\s*"(.*?)"/) || [])[1];
    const procedure = (raw.match(/procedure:\s*"(.*?)"/) || [])[1];
    const url = (raw.match(/url:\s*"(.*?)"/) || [])[1];
    if (id) {
        existingCampaigns.push({ clinicName, id, handle, procedure, url, raw });
    }
}

const finalCampaigns = [...userTweets];
const userIds = new Set(userTweets.map(c => c.id));
const userClinics = new Set(userTweets.map(c => c.clinicName));

for (const c of existingCampaigns) {
    if (userIds.has(c.id)) continue;
    if (userClinics.has(c.clinicName)) {
        const newerTweet = userTweets.find(nt => nt.clinicName === c.clinicName);
        if (/^\d+$/.test(c.id) && /^\d+$/.test(newerTweet.id)) {
            if (BigInt(c.id) < BigInt(newerTweet.id)) continue;
        }
    }
    finalCampaigns.push(c);
}

finalCampaigns.sort((a, b) => {
    const aVal = (/^\d+$/.test(a.id)) ? BigInt(a.id) : 0n;
    const bVal = (/^\d+$/.test(b.id)) ? BigInt(b.id) : 0n;
    if (bVal > aVal) return 1;
    if (bVal < aVal) return -1;
    // Fallback for non-numeric or equal
    return b.id.localeCompare(a.id);
});

const formatted = finalCampaigns.map(c => {
    return `            { clinicName: "${c.clinicName}", handle: "${c.handle}", procedure: "${c.procedure}", id: "${c.id}", url: "${c.url}" }`;
}).join(',\n');

console.log(formatted);
