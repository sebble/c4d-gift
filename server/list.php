<?php
$user = preg_replace('[^a-z]','',$_GET['user']);
echo `ls uploads/$user-*.22.wav`;
