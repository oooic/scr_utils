# デスクトップの整理、できてますか？  
MacbookProやMacbookAirでスクショを取ると、何故かデスクトップに保存される.  
とくに大学生諸賢は授業のオンライン化にともない、スクショをとる場面も格段に増えたのではないだろうか？  
期末試験の直前の忙しいときにデスクトップを埋め尽くす大量のスクショをひたすら仕分けるはめになったのは、少なくとも私だけではないはずだ。  
  
こんなお粗末な現状、デジタルネイティブと巷でもてはやされる我々らしくない。  
きっと奴がなんとかしてくれるはずだ。  
そう、我らがPythonなら！  
  
# tl;dr  
- Pythonでスクショを授業に合わせて自動振り分けできるツールを作ったよ！  
- daemon化してあるから、一回起動すれば電源を落とさない限り働いてくれるよ！  
- pipでインストールできるし、操作も簡単だからみんないれような！  
  
# はじめに  
改めまして、こんにちは。美味しいしです。  
今回は、Pythonを使ってスクショの自動整理ツールをつくってみました。  
  
できるだけ多くの人に使って欲しいとおもっているので、記事の前半で使い方、後半で実装に関して述べたいと思います。  
お忙しい方やとりあえず使えればいい、という方はgithubに簡潔な説明を載せているのでそちらをご覧ください。  
  
# インストール方法  
```sh  
Pip3 install Sukusho  
```  
で入ります。  
バグが見つかり次第修正版を上げていくので、たまに  
```sh  
Pip3 install Sukusho -U  
```  
してくれると嬉しいです。  
  
# 使い方  
まず、ターミナルを開いて、  
```sh  
sukushoinit  
```  
してください。  
すると、まず、
```sh  
sukushoinit  
```  
こんなふうにファイルをどこに保存したいかを聞かれます。デフォルトではデスクトップに保存されるようになっています。このままで良ければ、enterを、変更したい場合はそのフォルダまでの絶対パスを打ち込んでください。  
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
  
# 実装  
今回の実装は大きく分けて、  
- 設定ファイルの作成編集部分  
- ファイル操作部分  
- デーモン化部分  
- cli化の部分  
- pipできるようにする部分  
の5部構成となっています。  
  
これはpython-daemonというライブラリを使うと比較的容易に実装できます。  