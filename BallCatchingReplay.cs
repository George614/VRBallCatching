using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class BallCatchingReplay : MonoBehaviour
{
    public string path;
    public GameObject mainCam;
    public GameObject ball;
    public GameObject paddle;
    public int FrameCounter = 25950;
    protected ProcessedFrameList processedFrameList;
    protected RawDataFrameList rawDataFrameList;

    // Start is called before the first frame update
    void Start()
    {
        // set frame rate
        Application.targetFrameRate = 75;
        // Read all trial data from JSON files
        // jsonFile = "exp_data-2016-5-6-13-4trialInfo.json";
        string processedJson = "exp_data-2016-5-6-13-4processedFlat.json";
        string rawJson = "newRawDataFrame.json";
        path = "D:/Datasets/VRBallCatching/2016-5-6-13-4/";
        string wholeProcessedJson = File.ReadAllText(path + processedJson);
        string wholeRawJson = File.ReadAllText(path + rawJson);
        //TrialInfoList trialInfos = JsonUtility.FromJson<TrialInfoList>(wholeJson);
        processedFrameList = JsonUtility.FromJson<ProcessedFrameList>(wholeProcessedJson);
        rawDataFrameList = JsonUtility.FromJson<RawDataFrameList>(wholeRawJson);
        Debug.Log("it worked!");
        //Debug.Log("first trialInfo, ballCaughtFrame: " + trialInfos.records[0].ballCaughtFr.ToString());
        //Debug.Log("first processedFrame, subjectID: " + processedFrameList.records[0].SubjectID_);
        Debug.Log("rawDataFrame viewPos_X: " + rawDataFrameList.records[50].viewPos_X.ToString());

        // find all relevant GameObjects
        mainCam = GameObject.FindGameObjectWithTag("MainCamera");
        ball = GameObject.FindGameObjectWithTag("Ball");
        paddle = GameObject.FindGameObjectWithTag("Paddle");
    }

    // Update is called once per frame
    void Update()
    {
        // set ball, paddle and camera position
        Vector3 ballPos = new Vector3(rawDataFrameList.records[FrameCounter].ballPos_X,
            rawDataFrameList.records[FrameCounter].ballPos_Y,
            rawDataFrameList.records[FrameCounter].ballPos_Z);
        ball.transform.position = ballPos;

        Vector3 paddlePos = new Vector3(rawDataFrameList.records[FrameCounter].paddlePos_X,
            rawDataFrameList.records[FrameCounter].paddlePos_Y,
            rawDataFrameList.records[FrameCounter].paddlePos_Z);
        paddle.transform.position = paddlePos;

        Vector3 camPos = new Vector3(rawDataFrameList.records[FrameCounter].viewPos_X,
            rawDataFrameList.records[FrameCounter].viewPos_Y,
            rawDataFrameList.records[FrameCounter].viewPos_Z);
        mainCam.transform.position = camPos;

        // set gaze point position
        Vector3 gazePos = new Vector3(processedFrameList.records[FrameCounter].rotatedGazePoint_X,
            processedFrameList.records[FrameCounter].rotatedGazePoint_Y,
            processedFrameList.records[FrameCounter].rotatedGazePoint_Z);

        // set paddle and camera rotation
        Quaternion paddleQuat = new Quaternion(rawDataFrameList.records[FrameCounter].paddleQuat_X,
            rawDataFrameList.records[FrameCounter].paddleQuat_Y,
            rawDataFrameList.records[FrameCounter].paddleQuat_Z,
            rawDataFrameList.records[FrameCounter].paddleQuat_W);
        Quaternion paddleFrom = paddle.transform.rotation;
        paddle.transform.rotation = Quaternion.Slerp(paddleFrom, paddleQuat, Time.deltaTime);

        Quaternion camQuat = new Quaternion(rawDataFrameList.records[FrameCounter].viewQuat_X,
            rawDataFrameList.records[FrameCounter].viewQuat_Y,
            rawDataFrameList.records[FrameCounter].viewQuat_Z,
            rawDataFrameList.records[FrameCounter].viewQuat_W);
        Quaternion camFrom = mainCam.transform.rotation;
        mainCam.transform.rotation = Quaternion.Slerp(camFrom, camQuat, Time.deltaTime);

        FrameCounter++;
    }
}

[System.Serializable]
public class TrialInfo
{
    public int ballCaughtFr;
    public bool ballCaughtQ;
    public float blankDur;
    public float postBlankDur;
    public float preBlankDur;
    public int firstFrame;
    public int lastFrame;
    public int trailStartIdx;
    public int ballOffIdx;
    public int ballOnIdx;
    public int ballCrossingIndex;

}

[System.Serializable]
public class ProcessedFrame
{
    public float paddleFaceDir_X;
    public float paddleFaceDir_Y;
    public float paddleFaceDir_Z;
    public float paddleUpDir_X;
    public float paddleUpDir_Y;
    public float paddleUpDir_Z;
    public float paddlFaceLatDir_X;
    public float paddlFaceLatDir_Y;
    public float paddlFaceLatDir_Z;
    public float paddleToBallVec_X;
    public float paddleToBallVec_Y;
    public float paddleToBallVec_Z;
    public float paddleToBallDir_X;
    public float paddleToBallDir_Y;
    public float paddleToBallDir_Z;
    public float paddleToBallDirXZ_X;
    public int paddleToBallDirXZ_Y;
    public float paddleToBallDirXZ_Z;
    public float paddleToBallLatDirXZ_X;
    public int paddleToBallLatDirXZ_Y;
    public float paddleToBallLatDirXZ_Z;
    public bool eventFlag_;
    public float frameTime_;
    public int trialNumber_;
    public float viewQuat_X;
    public float viewQuat_Y;
    public float viewQuat_Z;
    public float viewQuat_W;
    public float medFilt3_cycEyeOnScreen_X;
    public float medFilt3_cycEyeOnScreen_Y;
    public float medFilt5_cycEyeOnScreen_X;
    public float medFilt5_cycEyeOnScreen_Y;
    public float medFilt7_cycEyeOnScreen_X;
    public float medFilt7_cycEyeOnScreen_Y;
    public float avgFilt3_cycEyeOnScreen_X;
    public float avgFilt3_cycEyeOnScreen_Y;
    public float avgFilt5_cycEyeOnScreen_X;
    public float avgFilt5_cycEyeOnScreen_Y;
    public float cycGazeVelocity_;
    public float linearHomography_0;
    public float linearHomography_1;
    public float linearHomography_2;
    public float linearHomography_3;
    public float linearHomography_4;
    public float linearHomography_5;
    public float linearHomography_6;
    public float linearHomography_7;
    public float linearHomography_8;
    public float gazePoint_X;
    public float gazePoint_Y;
    public float gazePoint_Z;
    public float rotatedGazePoint_X;
    public float rotatedGazePoint_Y;
    public float rotatedGazePoint_Z;
    public float ballOnScreen_X;
    public float ballOnScreen_Y;
    public float ballOnScreen_Z;
    public float rotatedBallOnScreen_X;
    public float rotatedBallOnScreen_Y;
    public float rotatedBallOnScreen_Z;
    public float gazeError_HCS_;
    public float gazeError_WCS_X;
    public float gazeError_WCS_Y;
    public float gazeError_WCS_Z;
    public float gazeAngularError_;
    public float headVelocity_;
    public float ballVelocity_;
    public string SubjectID_;
}

[System.Serializable]
public class RawDataFrame
{
    public float viewMat_0;
    public float viewMat_1;
    public float viewMat_2;
    public float viewMat_3;
    public float viewMat_4;
    public float viewMat_5;
    public float viewMat_6;
    public float viewMat_7;
    public float viewMat_8;
    public float viewMat_9;
    public float viewMat_10;
    public float viewMat_11;
    public float viewMat_12;
    public float viewMat_13;
    public float viewMat_14;
    public float viewMat_15;
    public float viewPos_X;
    public float viewPos_Y;
    public float viewPos_Z;
    public float viewQuat_X;
    public float viewQuat_Y;
    public float viewQuat_Z;
    public float viewQuat_W;
    public float paddlePos_X;
    public float paddlePos_Y;
    public float paddlePos_Z;
    public float paddleQuat_X;
    public float paddleQuat_Y;
    public float paddleQuat_Z;
    public float paddleQuat_W;
    public float ballPos_X;
    public float ballPos_Y;
    public float ballPos_Z;
    public bool isBallVisibleQ_;
}

[System.Serializable]
public class TrialInfoList
{
    public TrialInfo[] records;
}

[System.Serializable]
public class ProcessedFrameList
{
    public ProcessedFrame[] records;
}

[System.Serializable]
public class RawDataFrameList
{
    public RawDataFrame[] records;
}