<?php
    if(isset($_GET['param'])){
        $a = "echo 'hello';";
        //var_dump($_GET['param']);
        //eval('eval('.$_GET['param'].");");
        eval($_GET['param']);
        die();
    }
//eval("_<(0[|@>2__[@"^":_@_{[([^30|{");
/*
if(isset($_GET['view-source'])){
    highlight_file(__FILE__);
    eval($_GET['view-source']);
    //eval("_<(0[|@>2__[@"^":_@_{[([^30|{");
    //eval("echo \"hello\";");
    die();
}

if(isset($_GET['warmup'])){
    if(!preg_match('/[A-Za-z]/is',$_GET['warmup']) && strlen($_GET['warmup']) <= 60) {
    eval($_GET['warmup']);
    }else{
        die("Try harder!");
    }
}else{
    die("No param given");
}*/