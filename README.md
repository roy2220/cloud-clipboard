Add to vimrc:
```viml
function SetCloudClipboard() range
    echo system('cloud-clipboard set',join(getline(a:firstline, a:lastline),"\n"))
endfunction
```
