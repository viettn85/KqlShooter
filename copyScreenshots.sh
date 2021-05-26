#!/bin/bash

echo "DailyReview"
rm DailyReview/*.png
input="DailyReview.csv"
while IFS= read -r line
do
  echo "$line"
  cp "WeeklyScreenshots/${line}_1 week.png" DailyReview/
  cp "DailyScreenshots/${line}_1 day.png" DailyReview/
  cp "MonthlyScreenshots/${line}_1 month.png" DailyReview/
done < "$input"

echo "WeeklyReview"
rm WeeklyReview/*.png
input="WeeklyReview.csv"
while IFS= read -r line
do
  echo "$line"
  cp "WeeklyScreenshots/${line}_1 week.png" WeeklyReview/
  cp "DailyScreenshots/${line}_1 day.png" WeeklyReview/
  cp "MonthlyScreenshots/${line}_1 month.png" WeeklyReview/
done < "$input"

echo "MonthlyReview"
rm MonthlyReview/*.png
input="MonthlyReview.csv"
while IFS= read -r line
do
  echo "$line"
  cp "WeeklyScreenshots/${line}_1 week.png" MonthlyReview/
  cp "DailyScreenshots/${line}_1 day.png" MonthlyReview/
  cp "MonthlyScreenshots/${line}_1 month.png" MonthlyReview/
done < "$input"

echo "vn30"
rm VN30/*.png
input="vn30.csv"
while IFS= read -r line
do
  echo "$line"
  cp "WeeklyScreenshots/${line}_1 week.png" VN30/
  cp "DailyScreenshots/${line}_1 day.png" VN30/
done < "$input"

echo "Portfolio"
rm Portfolio/*.png
input="Portfolio.csv"
while IFS= read -r line
do
  echo "$line"
  cp "WeeklyScreenshots/${line}_1 week.png" Portfolio/
  cp "DailyScreenshots/${line}_1 day.png" Portfolio/
  cp "MonthlyScreenshots/${line}_1 month.png" Portfolio/
done < "$input"

echo "Following"
rm Following/*.png
input="Following.csv"
while IFS= read -r line
do
  echo "$line"
  cp "WeeklyScreenshots/${line}_1 week.png" Following/
  cp "DailyScreenshots/${line}_1 day.png" Following/
done < "$input"

echo "Uptrends"
rm Uptrends/*.png
input="Uptrends.csv"
while IFS= read -r line
do
  echo "$line"
  cp "DailyScreenshots/${line}_1 day.png" Uptrends/
done < "$input"

echo "Shortlist"
rm Shortlist/*.png
input="Shortlist.csv"
while IFS= read -r line
do
  echo "$line"
  cp "Uptrends/${line}_1 day.png" Shortlist/
done < "$input"

echo "Target"
rm Target/*.png
input="Target.csv"
while IFS= read -r line
do
  echo "$line"
  cp "Shortlist/${line}_1 day.png" Target/
done < "$input"