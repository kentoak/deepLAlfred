#!/bin/bash
auth_key=$DEEPL_AUTH_KEY || '';

PATH="$PATH:/usr/local/bin/"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PARSER="jq"
if ! type "$PARSER" >/dev/null 2>&1; then
  PARSER="${DIR}/jq-dist"
  xattr -dr com.apple.quarantine "$PARSER"
  chmod +x "$PARSER"
fi

function printJson() {
  echo '{"items": [{"uid": null,"arg": "'"$1"'","valid": "yes","autocomplete": "autocomplete","title": "'"$1"'"}]}'
}

query="$1"
target_lang="JA"
if echo "${query:0:20}" | ggrep -P '[\x{3041}-\x{3096}]' >/dev/null; then
  target_lang="EN"
fi
if echo "${query:0:20}" | ggrep -P '[\x{30A1}-\x{30FA}]' >/dev/null; then
  target_lang="EN"
fi
if echo "${query:0:20}" | ggrep -P '[々〇\x{3400}-\x{9FFF}\x{F900}-\x{FAFF}\x{20000}-\x{2FFFF}]' >/dev/null; then
  target_lang="EN"
fi
if echo "${query:0:20}" | ggrep -P '[\x{3001}-\x{301B}]' >/dev/null; then
  target_lang="EN"
fi


if [ -z "$1" ]; then
  echo "Home made DeepL CLI (${VERSION}; https://github.com/kentoak/deepLAlfred)"
  echo ""
  echo "SYNTAX : $0 [-l language] <query>" >&2
  echo "Example: $0 -l DE \"This is just an example.\""
  echo ""
  exit 1
fi

query="$1"
#query="$(echo "$query" | sed 's/\"/\\\"/g')" 
query="$(echo "$query" | gsed -E 's/\. ([a-z])/\. \U\1/g')"
query="$(echo "$query" | sed "s/\"/'/g")" 
query="$(echo "$query" | sed -e "s/[\r\n]\+/ /g")" #改行を半角スペースに
#query="$(echo "$query" | sed "s/'/\\\'/g")" 
query="$(echo "$query" | sed "s/& /%26%20/g")" 
query="$(echo "$query" | sed "s/% /%25%20/g")"
query="$(echo "$query" | sed "s/¼/=/g")"
query="$(echo "$query" | sed "s/´/'/g")"
query="$(echo "$query" | sed -e "s/[\r\n]\+//g")"
query="$(echo "$query" | iconv -f utf-8-mac -t utf-8 | xargs)"           

result=$(curl -s -H 'Content-Type:application/x-www-form-urlencoded' -POST https://api-free.deepl.com/v2/translate -d "auth_key=${auth_key}" -d "text=${query}" -d "target_lang=$target_lang")

if [[ $result == *'"error":{"code":'* ]]; then
  message=$(echo "$result" | "$PARSER" -r '.["error"]|.message')
  printJson "Error: $message"
else
  sts=$(echo "$result" | "$PARSER" -r ".translations[0].text") 
  #sts="$(echo "$sts" | sed 's/\"/\\\"/g')" 
  ssts="$(echo "$sts" | sed "s/\"/”/g")"
  sts="$(echo "$sts" | sed 's/．/。/g' | sed 's/，/、/g')" 
  sts1="$sts"
  cnt1="$(echo "$sts" | wc -m | bc)"
  CNT=$cnt1
  myQuery=$query 
  myQuery="$(echo "$myQuery" | sed 's/%26/\&/g')" 
  myQuery="$(echo "$myQuery" | sed 's/%25/\%/g')" 
  myQuery="$(echo "$myQuery" | sed 's/%20/ /g')"
  #myQuery="$(echo "$myQuery" | sed 's/\"/\\\"/g')"
  myQuery="$(echo "$myQuery" | sed "s/\"/'/g")"
  cnt2="$(echo "$myQuery" | wc -m | bc)"
  if [[ ${query:0:20} != ${sts:0:20} ]]; then
    if [[ $target_lang == "JA" ]]; then 
      sts="$(echo "$sts" | sed 'y/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９/')"
      numForTitle=40
      if [[ $cnt1 -gt $(($numForTitle+1)) ]]; then 
        start=0
        startForSubtitle=0
        MM=()
        numForSubtitle=83
        numForTitle=40
        subtitleFinish=false
        cnt1LastFlag=false
        k=0
        while [ 1 ]
        do
          k=$((k+1))
          cnt1=`expr $cnt1 - $numForTitle`
          if [[ $cnt1 -gt 0 ]]; then
            now=${sts:$((start)):$((numForTitle))} 
            now1=${sts1:$((start)):$((numForTitle))}
          else
            now=${sts:$((start))}
            now1=${sts1:$((start))}
          fi
          cntForEnd="$(echo "${myQuery:$((startForSubtitle))}" | wc -m | bc)"
          endend=$numForSubtitle
          if [[ $cntForEnd -gt $numForSubtitle ]]; then
            for ((i=0; i < $numForSubtitle; i++)); do
              if [[ $i -eq 0 ]]; then
                endbreak=${myQuery:$((startForSubtitle+endend-1)):1}
                if [[ $endbreak == " " ]]; then
                  break
                fi
              else
                endbreak=${myQuery:$((startForSubtitle+endend-1)):1}
                if [[ $endbreak == " " ]]; then
                  break
                fi
                endend=$((endend-1))
              fi
            done
            nowForSubtitle=${myQuery:$((startForSubtitle)):$((endend))}
          fi
          cnt2=`expr $cnt2 - $endend`
          if [[ $start == 0 ]]; then 
            if [[ $cnt2 -gt 0 ]]; then
              a='{"title":"'$now'","arg":"'$sts1'","subtitle":"'$nowForSubtitle'"},'
            else
              a='{"title":"'$now'","arg":"'$sts1'","subtitle":"'${myQuery:$((startForSubtitle))}'"},'
              subtitleFinish=true
            fi
          else 
            if [[ $cnt1 -gt 0 ]]; then
              if [[ $cnt2 -gt 0 ]]; then
                a='{"title":"'$now'","arg":"'$now1'","subtitle":"'$nowForSubtitle'"},'
              else
                a='{"title":"'$now'","arg":"'$now1'","subtitle":"'${myQuery:$((startForSubtitle))}'"},'
              fi
            else
              if [[ $cnt2 -gt 0 ]]; then
                if [[ ${cnt1LastFlag} == false ]]; then
                  a='{"title":"'$now'","arg":"'$now1'","subtitle":"'$nowForSubtitle'"},'
                  cnt1LastFlag=true
                else
                  a='{"title":"","arg":"","subtitle":"'$nowForSubtitle'"},'
                fi
              else
                if [[ $tmpStart == $start ]]; then 
                  a='{"title":"","arg":"","subtitle":"'${myQuery:$((startForSubtitle))}'"}'
                else
                  if "${subtitleFinish}"; then
                    a='{"title":"'$now'","arg":"'$now1'","subtitle":""}'
                  else
                    a='{"title":"'$now'","arg":"'$now1'","subtitle":"'${myQuery:$((startForSubtitle))}'"}'
                  fi
                fi
              fi
            fi
          fi
          startForSubtitle=`expr $startForSubtitle + $endend`
          tmpStart=$start
          if [[ `expr $tmpStart + $numForTitle` -le CNT ]]; then
            start=`expr $tmpStart + $numForTitle`
          else
            start=$tmpStart
          fi
          MM+=($a)
          if [[ $cnt1 -lt 0 ]] && [[ $cnt2 -lt 0 ]]; then
            break
          fi
          if [[ $k -gt 20 ]]; then #無限ループ回避
              break
          fi
        done
        mo=${MM[@]}
        echo '{"items":['$mo']}' | "$PARSER" -r -R .
      else 
        numForSubtitle=83
        cnt2="$(echo "$myQuery" | wc -m | bc)"
        startForSubtitle=0
        if [[ $cnt2 -gt $numForSubtitle ]]; then 
          k=0
          while [ 1 ]
          do
            k=$((k+1))
            cnt2=`expr $cnt2 - $numForSubtitle`
            if [[ $cnt2 -gt 0 ]]; then
              endend=$numForSubtitle
              for ((i=0; i < $numForSubtitle; i++)); do
                if [[ $i -eq 0 ]]; then
                  endbreak=${myQuery:$((startForSubtitle+endend-1)):1}
                  if [[ $endbreak == " " ]]; then
                    break
                  fi
                else
                  endbreak=${myQuery:$((startForSubtitle+endend-1)):1}
                  if [[ $endbreak == " " ]]; then
                    break
                  fi
                  endend=$((endend-1))
                fi
              done
              nowForSubtitle=${myQuery:$((startForSubtitle)):$((endend))}
            fi
            if [[ $cnt2 -gt 0 ]]; then 
              a='{"title":"'$sts'","arg":"'$sts'","subtitle":"'$nowForSubtitle'"},'
            else
              a='{"title":"","arg":"","subtitle":"'${myQuery:$((startForSubtitle))}'"}'
            fi
            startForSubtitle=`expr $startForSubtitle + $endend`
            MM+=($a)
            if [[ $cnt2 -lt 0 ]]; then
              break
            fi
            if [[ $k -gt 20 ]]; then #無限ループ回避
              break
            fi
          done
          mo=${MM[@]}
          echo '{"items":['$mo']}' | "$PARSER" -r -R .
        else
          a='{"title":"'$sts'","arg":"'$sts1'","subtitle":"'$myQuery'"}'
          echo '{"items":['$a']}' | "$PARSER" -r -R .
        fi
      fi
    else
      numForTitle=83
      numForSubtitle=39
      if [[ $cnt1 -gt $(($numForTitle+1)) ]]; then
        start=0
        MM=()
        u=-1
        k=0
        while [ 1 ]
        do
          u=$((u+1))
          k=$((k+1))
          cnt1=`expr $cnt1 - $numForTitle`
          if [[ $cnt1 -gt 0 ]]; then
            endend=$numForTitle
            for ((i=0; i < $numForTitle; i++)); do
              if [[ $i -eq 0 ]]; then
                endbreak=${sts:$((start+endend-1)):$((1))}
                if [[ $endbreak == " " ]]; then
                  break
                fi
              else
                endbreak=${sts:$((start+endend-1)):$((1))}
                if [[ $endbreak == " " ]]; then
                  break
                fi
                endend=$((endend-1))
              fi
            done
            numForTitle=$endend
            now=${sts:$((start)):$((endend))}
          else
            now=${sts:$((start))}
          fi
          if [[ $start == 0 ]]; then
            a='{"title":"'$now'","arg":"'$sts'","subtitle":"'${myQuery:$numForSubtitle*u:$numForSubtitle}'"},'
          else
            if [[ $cnt1 -gt 0 ]]; then
              a='{"title":"'$now'","arg":"'$now'","subtitle":"'${myQuery:$numForSubtitle*u:$numForSubtitle}'"},'
            else
              a='{"title":"'$now'","arg":"'$now'","subtitle":"'${myQuery:$numForSubtitle*u:$numForSubtitle}'"}'
            fi
          fi
          start=`expr $start + $endend`
          MM+=($a)
          if [[ $cnt1 -lt 0 ]]; then
            break
          fi
          if [[ $k -gt 20 ]]; then #無限ループ回避
              break
          fi
        done
        mo=${MM[@]}
        echo '{"items":['$mo']}' | "$PARSER" -r -R .
      else
        a='{"title":"'$sts'","arg":"'$sts1'","subtitle":"'$myQuery'"}'
        echo '{"items":['$a']}' | "$PARSER" -r -R .
      fi
    fi
  else
  a='{"title":"'$sts'","arg":"'$sts1'","subtitle":"'$myQuery'"}'
  echo '{"items":['$a']}' | "$PARSER" -r -R .
  fi
fi
