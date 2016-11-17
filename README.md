Add to vimrc:
```viml
" for CloudClipboard
function SetCloudClipboard() range
    echo system('cloud-clipboard set',join(getline(a:firstline, a:lastline),"\n"))
endfunction

vnoremap <silent> <leader>y :call SetCloudClipboard()<CR>
```
