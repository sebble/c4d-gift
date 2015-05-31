<?php

foreach(array('video', 'audio') as $type) {
    if (isset($_FILES["${type}-blob"])) {

        $fileName = $_POST["${type}-filename"];
        $uploadDirectory = 'uploads/'.$fileName;

        $finfo = finfo_open(FILEINFO_MIME_TYPE);
        $mime = finfo_file($finfo, $_FILES["${type}-blob"]['tmp_name']);
        finfo_close($finfo);
        echo $mime."\n";

        $ext = 'audio';
        if ($mime == 'audio/x-wav') {
            $ext = 'wav';
        }
        if ($mime == 'application/ogg') {
            $ext = 'ogg';
        }

        $r = rand(10000,99999);
        $f = 'uploads/sam-'.$r.'.'.$ext;
        
        `touch $f.touch`;

        if (!move_uploaded_file($_FILES["${type}-blob"]["tmp_name"], $f)) {
            echo(" problem moving uploaded file");
        } else {
            `opusdec $f $f.wav`;
            `ffmpeg -i $f.wav -acodec pcm_s16le -ac 1 -ar 22050 $f.22.wav`;
            `normalize-audio -g 20dB $f.22.wav`;
        }

        echo($uploadDirectory);
    }
}
?>
