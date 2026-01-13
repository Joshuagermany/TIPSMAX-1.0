"""
인증 라우트
카카오, 구글, 네이버 소셜 로그인 처리
"""

import os
import httpx
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()

# 카카오 OAuth 설정
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY", "")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET", "")  # Client Secret이 활성화된 경우 필요
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI", "http://localhost:5173/login?provider=kakao")

# 환경 변수 로드 확인 로그 (카카오)
if KAKAO_CLIENT_SECRET:
    logger.info(f"카카오 Client Secret 로드됨 (길이: {len(KAKAO_CLIENT_SECRET)})")
else:
    logger.warning("카카오 Client Secret이 설정되지 않았습니다. .env 파일을 확인하세요.")

# 구글 OAuth 설정
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:5173/login?provider=google")

# 네이버 OAuth 설정
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")
NAVER_REDIRECT_URI = os.getenv("NAVER_REDIRECT_URI", "http://localhost:5173/login?provider=naver")


class KakaoTokenRequest(BaseModel):
    code: str


class KakaoTokenResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None
    expires_in: int
    refresh_token_expires_in: int | None = None


class GoogleTokenRequest(BaseModel):
    code: str


class NaverTokenRequest(BaseModel):
    code: str
    state: str | None = None


@router.get("/kakao/login")
async def kakao_login():
    """카카오 로그인 페이지로 리다이렉트"""
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?client_id={KAKAO_REST_API_KEY}"
        f"&redirect_uri={KAKAO_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=profile_nickname,account_email"  # 닉네임과 이메일 정보 요청
    )
    return RedirectResponse(url=kakao_auth_url)


@router.post("/kakao/callback")
async def kakao_callback(request: KakaoTokenRequest):
    """카카오 인증 코드를 받아서 액세스 토큰 발급"""
    logger.info(f"카카오 로그인 콜백 요청 - code: {request.code[:20]}...")
    try:
        # 카카오 토큰 발급 요청
        async with httpx.AsyncClient() as client:
            logger.info(f"카카오 토큰 발급 요청 - redirect_uri: {KAKAO_REDIRECT_URI}, client_id: {KAKAO_REST_API_KEY[:10]}...")
            
            # 토큰 요청 데이터 준비
            token_data = {
                "grant_type": "authorization_code",
                "client_id": KAKAO_REST_API_KEY,
                "redirect_uri": KAKAO_REDIRECT_URI,
                "code": request.code,
            }
            
            # Client Secret이 설정되어 있으면 추가
            if KAKAO_CLIENT_SECRET:
                token_data["client_secret"] = KAKAO_CLIENT_SECRET
                logger.info("Client Secret 사용")
            else:
                logger.info("Client Secret 미사용 (기본 설정)")
            
            token_response = await client.post(
                "https://kauth.kakao.com/oauth/token",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            logger.info(f"카카오 토큰 응답 상태: {token_response.status_code}")
            if token_response.status_code != 200:
                error_text = token_response.text
                error_data = token_response.json() if token_response.headers.get("content-type", "").startswith("application/json") else {}
                error_code = error_data.get("error_code", "")
                error_description = error_data.get("error_description", "")
                
                logger.error(f"카카오 토큰 발급 실패: {error_text}")
                logger.error(f"  - Error Code: {error_code}")
                logger.error(f"  - Error Description: {error_description}")
                logger.error(f"  - Client Secret 사용 여부: {'사용' if KAKAO_CLIENT_SECRET else '미사용'}")
                logger.error(f"  - Redirect URI: {KAKAO_REDIRECT_URI}")
                
                # KOE010 오류에 대한 구체적인 안내
                if error_code == "KOE010":
                    detail_msg = (
                        f"카카오 클라이언트 자격 증명 오류 (KOE010)\n"
                        f"가능한 원인:\n"
                        f"1. 카카오 개발자 콘솔에서 Client Secret이 활성화되어 있는데 제공하지 않음\n"
                        f"   → 해결: 환경 변수 KAKAO_CLIENT_SECRET 설정 또는 카카오 콘솔에서 Client Secret 비활성화\n"
                        f"2. REST API KEY가 잘못되었거나 만료됨\n"
                        f"   → 해결: 카카오 개발자 콘솔에서 REST API KEY 확인\n"
                        f"3. Redirect URI가 카카오 개발자 콘솔에 등록된 것과 일치하지 않음\n"
                        f"   → 해결: 카카오 개발자 콘솔의 Redirect URI와 '{KAKAO_REDIRECT_URI}' 일치 확인\n"
                        f"\n자세한 내용은 KAKAO_LOGIN_ERROR_SOLUTION.md 참고"
                    )
                else:
                    detail_msg = f"카카오 토큰 발급 실패: {error_text}"
                
                raise HTTPException(
                    status_code=400,
                    detail=detail_msg
                )

            token_data = token_response.json()
            access_token = token_data.get("access_token")
            logger.info(f"카카오 액세스 토큰 발급 성공")

            # 카카오 사용자 정보 조회 (필요한 정보를 명시적으로 요청)
            user_response = await client.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
                params={
                    "property_keys": '["kakao_account.profile.nickname","kakao_account.profile.profile_image_url","kakao_account.email"]'
                }
            )

            logger.info(f"카카오 사용자 정보 응답 상태: {user_response.status_code}")
            if user_response.status_code != 200:
                error_text = user_response.text
                logger.error(f"카카오 사용자 정보 조회 실패: {error_text}")
                raise HTTPException(
                    status_code=400,
                    detail=f"카카오 사용자 정보 조회 실패: {error_text}"
                )

            user_data = user_response.json()
            logger.info(f"카카오 사용자 정보 조회 성공 - id: {user_data.get('id')}")
            logger.info(f"카카오 사용자 정보 전체 응답: {user_data}")  # 디버깅용
            
            # 카카오 계정 정보 추출
            kakao_account = user_data.get("kakao_account", {})
            profile = kakao_account.get("profile", {})
            
            # 닉네임 추출 (여러 경로 시도)
            nickname = (
                profile.get("nickname") or 
                kakao_account.get("profile", {}).get("nickname") or
                kakao_account.get("name") or 
                None
            )
            
            # 닉네임이 없으면 사용자 ID를 사용하거나 기본값 사용
            if not nickname:
                logger.warning(f"카카오 닉네임을 찾을 수 없습니다. user_data: {user_data}")
                nickname = f"카카오 사용자 {user_data.get('id', '')}"
            
            result = {
                "success": True,
                "user": {
                    "id": user_data.get("id"),
                    "nickname": nickname,
                    "email": kakao_account.get("email"),
                    "profile_image": profile.get("profile_image_url") or kakao_account.get("profile", {}).get("profile_image_url"),
                },
                "access_token": access_token,  # 임시 (추후 JWT로 교체)
            }
            logger.info(f"카카오 로그인 성공 - 사용자: {result['user']['nickname']}")
            return result

    except HTTPException:
        raise
    except httpx.HTTPError as e:
        logger.error(f"카카오 API 호출 오류: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"카카오 API 호출 오류: {str(e)}")
    except Exception as e:
        logger.error(f"카카오 로그인 처리 오류: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"카카오 로그인 처리 오류: {str(e)}")


@router.get("/google/login")
async def google_login():
    """구글 로그인 페이지로 리다이렉트"""
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
        f"&access_type=offline"
    )
    return RedirectResponse(url=google_auth_url)


@router.post("/google/callback")
async def google_callback(request: GoogleTokenRequest):
    """구글 인증 코드를 받아서 액세스 토큰 발급"""
    logger.info(f"구글 로그인 콜백 요청 - code: {request.code[:20]}...")
    try:
        # 구글 토큰 발급 요청
        async with httpx.AsyncClient() as client:
            logger.info(f"구글 토큰 발급 요청 - redirect_uri: {GOOGLE_REDIRECT_URI}")
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": request.code,
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uri": GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            logger.info(f"구글 토큰 응답 상태: {token_response.status_code}")
            if token_response.status_code != 200:
                error_text = token_response.text
                logger.error(f"구글 토큰 발급 실패: {error_text}")
                raise HTTPException(
                    status_code=400,
                    detail=f"구글 토큰 발급 실패: {error_text}"
                )

            token_data = token_response.json()
            access_token = token_data.get("access_token")
            logger.info(f"구글 액세스 토큰 발급 성공")

            # 구글 사용자 정보 조회
            user_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            logger.info(f"구글 사용자 정보 응답 상태: {user_response.status_code}")
            if user_response.status_code != 200:
                error_text = user_response.text
                logger.error(f"구글 사용자 정보 조회 실패: {error_text}")
                raise HTTPException(
                    status_code=400,
                    detail=f"구글 사용자 정보 조회 실패: {error_text}"
                )

            user_data = user_response.json()
            logger.info(f"구글 사용자 정보 조회 성공 - id: {user_data.get('id')}")
            
            result = {
                "success": True,
                "user": {
                    "id": user_data.get("id"),
                    "nickname": user_data.get("name") or user_data.get("email", "").split("@")[0] or "구글 사용자",
                    "email": user_data.get("email"),
                    "profile_image": user_data.get("picture"),
                },
                "access_token": access_token,  # 임시 (추후 JWT로 교체)
            }
            logger.info(f"구글 로그인 성공 - 사용자: {result['user']['nickname']}")
            return result

    except HTTPException:
        raise
    except httpx.HTTPError as e:
        logger.error(f"구글 API 호출 오류: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"구글 API 호출 오류: {str(e)}")
    except Exception as e:
        logger.error(f"구글 로그인 처리 오류: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"구글 로그인 처리 오류: {str(e)}")


@router.get("/naver/login")
async def naver_login():
    """네이버 로그인 페이지로 리다이렉트"""
    if not NAVER_CLIENT_ID or not NAVER_REDIRECT_URI:
        logger.error("네이버 OAuth 설정이 완료되지 않았습니다. NAVER_CLIENT_ID / NAVER_REDIRECT_URI 확인 필요")
        raise HTTPException(status_code=500, detail="네이버 OAuth 설정이 완료되지 않았습니다. 서버 환경 변수를 확인하세요.")

    # 간단한 state 값 (실서비스에서는 난수/세션 기반으로 검증 필요)
    state = "tipsmax_naver_state"

    naver_auth_url = (
        "https://nid.naver.com/oauth2.0/authorize"
        f"?response_type=code"
        f"&client_id={NAVER_CLIENT_ID}"
        f"&redirect_uri={NAVER_REDIRECT_URI}"
        f"&state={state}"
    )
    return RedirectResponse(url=naver_auth_url)


@router.post("/naver/callback")
async def naver_callback(request: NaverTokenRequest):
    """네이버 인증 코드를 받아서 액세스 토큰 발급"""
    logger.info(f"네이버 로그인 콜백 요청 - code: {request.code[:20]}..., state: {request.state}")
    try:
        if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET or not NAVER_REDIRECT_URI:
            logger.error("네이버 OAuth 설정이 완료되지 않았습니다. NAVER_CLIENT_ID / NAVER_CLIENT_SECRET / NAVER_REDIRECT_URI 확인 필요")
            raise HTTPException(status_code=500, detail="네이버 OAuth 설정이 완료되지 않았습니다. 서버 환경 변수를 확인하세요.")

        async with httpx.AsyncClient() as client:
            logger.info(
                f"네이버 토큰 발급 요청 - redirect_uri: {NAVER_REDIRECT_URI}, client_id: {NAVER_CLIENT_ID[:8]}..., state: {request.state}"
            )

            # 네이버 토큰 발급 요청
            token_response = await client.post(
                "https://nid.naver.com/oauth2.0/token",
                params={
                    "grant_type": "authorization_code",
                    "client_id": NAVER_CLIENT_ID,
                    "client_secret": NAVER_CLIENT_SECRET,
                    "code": request.code,
                    "state": request.state or "tipsmax_naver_state",
                    "redirect_uri": NAVER_REDIRECT_URI,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            logger.info(f"네이버 토큰 응답 상태: {token_response.status_code}")
            if token_response.status_code != 200:
                error_text = token_response.text
                logger.error(f"네이버 토큰 발급 실패: {error_text}")
                raise HTTPException(
                    status_code=400,
                    detail=f"네이버 토큰 발급 실패: {error_text}",
                )

            token_data = token_response.json()
            access_token = token_data.get("access_token")
            logger.info("네이버 액세스 토큰 발급 성공")

            # 네이버 사용자 정보 조회
            user_response = await client.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            logger.info(f"네이버 사용자 정보 응답 상태: {user_response.status_code}")
            if user_response.status_code != 200:
                error_text = user_response.text
                logger.error(f"네이버 사용자 정보 조회 실패: {error_text}")
                raise HTTPException(
                    status_code=400,
                    detail=f"네이버 사용자 정보 조회 실패: {error_text}",
                )

            user_data = user_response.json()
            logger.info(f"네이버 사용자 정보 전체 응답: {user_data}")

            naver_user = user_data.get("response", {}) or {}

            # 닉네임/이름 추출
            nickname = (
                naver_user.get("name")
                or naver_user.get("nickname")
                or (naver_user.get("email") or "").split("@")[0]
                or None
            )

            if not nickname:
                logger.warning(f"네이버 닉네임을 찾을 수 없습니다. naver_user: {naver_user}")
                nickname = f"네이버 사용자 {naver_user.get('id', '')}"

            result = {
                "success": True,
                "user": {
                    "id": naver_user.get("id"),
                    "nickname": nickname,
                    "email": naver_user.get("email"),
                    "profile_image": naver_user.get("profile_image"),
                },
                "access_token": access_token,  # 임시 (추후 JWT로 교체)
            }
            logger.info(f"네이버 로그인 성공 - 사용자: {result['user']['nickname']}")
            return result

    except HTTPException:
        raise
    except httpx.HTTPError as e:
        logger.error(f"네이버 API 호출 오류: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"네이버 API 호출 오류: {str(e)}")
    except Exception as e:
        logger.error(f"네이버 로그인 처리 오류: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"네이버 로그인 처리 오류: {str(e)}")
