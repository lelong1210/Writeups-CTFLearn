<?php
class point {
    public $x;
    public $y;
    public $ID;

    public function __construct($x, $y, $ID) {
        $this->x = $x;
        $this->y = $y;
        $this->ID = $ID;
    }
}

$object = new point('0','0',"whoami");
$serialized = serialize($object);
echo $serialized;
