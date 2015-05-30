<?php
foreach(array('video', 'audio') as $type) {
    if (isset($_FILES["${type}-blob"])) {

        $fileName = $_POST["${type}-filename"];
        $uploadDirectory = 'uploads/'.$fileName;

        $r = rand(10000,99999);
        $f = 'uploads/sam-'.$r.'.wav';

        if (!move_uploaded_file($_FILES["${type}-blob"]["tmp_name"], $f)) {
            echo(" problem moving uploaded file");
        }

        echo($uploadDirectory);
    }
}
?>
