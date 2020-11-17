[![Downloads](https://pepy.tech/badge/sukusho)](https://pepy.tech/project/sukusho)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)
# Sukusho
MacbookPro及びMacbookAir向けスクショクリーナー。

## インストール方法  
```sh  
Pip3 install Sukusho  
```  
で入ります。  
バグが見つかり次第修正版を上げていくので、たまに  
```sh  
Pip3 install Sukusho -U  
```  
してくれると嬉しいです。  
  
## 使い方  
まず、ターミナルを開いて、  
```sh  
sukushoinit  
```  
してください。  
するとまず、
``` 
[now:~/Desktop]:press enter or input savedir path 
```  
と言うようにファイルをどこに保存したいかを聞かれます。デフォルトではデスクトップに保存されるようになっています。このままで良ければ、enterを、変更したい場合はそのフォルダまでの絶対パスを打ち込んでください。  
次に、こんなふうにエクセルがでてくるはずです。  
ここに履修している授業をこんな風に打ち込みましょう。  
空きコマは空白にしてください。  
さて、テストを走らせてみましょう。  
```sh  
sukusho -t  
```  
ここで、  
> Your sukusho is ready!  

と出てきたらOKです！  
いよいよ稼働させます。  
```sh  
sukusho -start  
```  
と打ち込めば、システムが走り始めます！  
システムを止めたい場合には、  
```sh  
sukusho -kill  
```  
と打ち込みましょう。  
保存先を変えたい場合は  
```sh  
sukusho -es  
```  
時間割を変えたい場合は、  
```sh  
sukusho -ej  
```  
で行うことができます。  
