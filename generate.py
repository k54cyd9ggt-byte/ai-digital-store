from pathlib import Path
import csv, json, random, zipfile
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
SECTORS={
 'cafe':('カフェ','季節のおすすめ','ほっと一息つく時間を','店頭でメニューをご確認ください'),
 'beauty':('美容サロン','施術メニュー','自分をいたわる時間を','ご予約前に内容をご確認ください'),
 'shop':('雑貨ショップ','新着アイテム','毎日に小さな楽しみを','商品詳細をご覧ください')}
ANGLES=['新着紹介','使い方','よくある質問','スタッフのおすすめ','季節の話題','選び方','利用シーン','お客様へのお知らせ','ブランドの想い','週末の提案']
TEMPLATES=['{topic}をテーマに、{item}をご紹介。{benefit}。{cta}。','今日は{topic}。{item}の魅力をわかりやすくお届けします。{cta}。','{topic}が気になる方へ。{benefit}。{item}については{cta}。']

def build(seed=42):
 random.seed(seed)
 catalog=[]
 for sector,(label,item,benefit,cta) in SECTORS.items():
  folder=OUT/sector; folder.mkdir(exist_ok=True)
  rows=[]
  for i in range(1,101):
   angle=ANGLES[(i-1)%len(ANGLES)]
   post=random.choice(TEMPLATES).format(topic=angle,item=item,benefit=benefit,cta=cta)
   rows.append({'No':i,'テーマ':angle,'投稿文':post,'画像アイデア':f'{label}の{angle}を表す写真と余白のある見出し','推奨CTA':cta,'確認事項':'実際の商品・価格・営業情報に合わせて編集'})
  with (folder/'posts.csv').open('w',encoding='utf-8-sig',newline='') as f:
   w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
  (folder/'README.txt').write_text(f'{label}向けSNS投稿アイデア100件\n\nCSVをExcel等で開き、固有の商品名・事実を確認して編集してください。\n架空の効果、レビュー、値引き、在庫情報は記載しないでください。\nテンプレートの重複や表現の単調さがあるため、販売前に品質を確認してください。\n',encoding='utf-8')
  archive=OUT/f'{sector}-social-posts.zip'
  with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
   z.write(folder/'posts.csv','posts.csv');z.write(folder/'README.txt','README.txt')
  catalog.append({'slug':sector,'title':f'{label}向けSNS投稿文100本','suggested_price_jpy':980,'file':archive.name,'sample':rows[:3]})
 (OUT/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Generated 3 ZIP products and catalog.json')
if __name__=='__main__':build()
