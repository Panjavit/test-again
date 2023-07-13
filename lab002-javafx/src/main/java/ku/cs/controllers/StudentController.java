package ku.cs.controllers;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import ku.cs.models.Student;

public class StudentController {
    @FXML
    Label nameLabel;
    @FXML
    Label idLabel;
    @FXML
    Label scoreLabel;

    @FXML
    public void initialize() {
        Student student = new Student("6510450615", "Panjavit Oranpitiphan");
        showStudent(student);
    }

    private void showStudent(Student student) {
        nameLabel.setText(student.getName());
        idLabel.setText(student.getId());
        //scoreLabel.setText(""+student.getScore());
        scoreLabel.setText(String.format("%.2f",student.getScore()));
    }

    @FXML
    protected void onHandButtonClink(){
        System.out.println("It's Work");
    }
}