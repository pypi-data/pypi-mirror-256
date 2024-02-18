import {useContext} from "react";
import {AppContext} from "../../App";
import SingleCell from "./SingleCell";

export function ExecutedCodePanel() {
    const props = useContext(AppContext);

    const length = props!.selectedCommit!.historyExecCells.length;

    return (
        <div>
            {props!.selectedCommit!.historyExecCells.map((code, i) => (
                <div key={i}>
                    <SingleCell execNumber={(length - i).toString()} content={code.content} cssClassNames={"notebook"}/>
                    <br/>
                </div>
            ))}
        </div>
    );
}
