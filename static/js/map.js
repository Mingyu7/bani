// 지도 위젯 스크립트
const mapContainer = document.getElementById('map');

// 위치 정보 가져오기 성공 시
const onSuccess = (position) => {
    const { latitude, longitude } = position.coords;
    const mapOption = {
        center: new kakao.maps.LatLng(latitude, longitude), // 현재 위치를 중심으로 설정
        level: 3
    };
    const map = new kakao.maps.Map(mapContainer, mapOption);

    // 현재 위치에 마커 생성
    const markerPosition = new kakao.maps.LatLng(latitude, longitude);
    const marker = new kakao.maps.Marker({
        position: markerPosition
    });
    marker.setMap(map);
};

// 위치 정보 가져오기 실패 시
const onError = () => {
    mapContainer.innerHTML = "<p style='text-align: center; padding-top: 50px;'>위치 정보를 가져올 수 없어 지도를 표시할 수 없습니다.</p>";
};

// 브라우저에서 위치 정보 지원하는지 확인 후, 위치 정보 요청
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(onSuccess, onError);
} else {
    mapContainer.innerHTML = "<p style='text-align: center; padding-top: 50px;'>이 브라우저에서는 위치 정보를 지원하지 않습니다.</p>";
}