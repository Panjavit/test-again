module ku.cs.lab002javafx {
    requires javafx.controls;
    requires javafx.fxml;


    opens ku.cs.lab002javafx to javafx.fxml;
    exports ku.cs.lab002javafx;
    exports ku.cs.controllers;
    opens ku.cs.controllers to javafx.fxml;
}