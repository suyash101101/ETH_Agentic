from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from ...services.file_service import CircuitFileService

router = APIRouter()
file_service = CircuitFileService("./app/zk_circuits/build")

@router.get("/circuit/{circuit_name}/wasm")
async def get_wasm(circuit_name: str):
    try:
        if not file_service.verify_circuit_files(circuit_name):
            raise HTTPException(status_code=404, detail="Circuit files not found")
        
        wasm_path = file_service.get_circuit_paths(circuit_name)["wasm"]
        return FileResponse(
            path=wasm_path,
            media_type="application/wasm",
            filename=f"{circuit_name}.wasm"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/circuit/{circuit_name}/zkey")
async def get_zkey(circuit_name: str):
    try:
        zkey_path = file_service.get_circuit_paths(circuit_name)["zkey"]
        if not zkey_path.exists():
            raise HTTPException(status_code=404, detail="ZKEY file not found")
        return FileResponse(
            path=zkey_path,
            media_type="application/octet-stream",
            filename=f"{circuit_name}.zkey"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/circuit/{circuit_name}/vkey")
async def get_vkey(circuit_name: str):
    try:
        vkey_path = file_service.get_circuit_paths(circuit_name)["vkey"]
        if not vkey_path.exists():
            raise HTTPException(status_code=404, detail="Verification key not found")
        return FileResponse(
            path=vkey_path,
            media_type="application/json",
            filename=f"verification_key_{circuit_name}.json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/circuits")
async def list_circuits():
    try:
        circuits = file_service.list_available_circuits()
        return JSONResponse(content={"circuits": circuits})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))