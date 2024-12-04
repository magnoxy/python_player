import cv2

def selecionar_roi_video_dinamico(cap):
    print("Pressione 'c' para selecionar uma ROI ou 'q' para sair do vídeo.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo.")
            break

        cv2.imshow("Vídeo", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("Saindo")
            break

        if key == ord('c'):
            print("Selecione a região de interesse (ROI) na janela e pressione ENTER para confirmar ou ESC para cancelar.")
            roi = cv2.selectROI("Selecione a ROI", frame, fromCenter=False, showCrosshair=True)
            cv2.destroyWindow("Selecione a ROI")

            if roi == (0, 0, 0, 0):
                print("Nenhuma ROI foi selecionada.")
                continue

            x, y, w, h = roi
            roi_cortada = frame[int(y):int(y+h), int(x):int(x+w)]

            cv2.imshow("ROI Cortada", roi_cortada)
            print("Pressione qualquer tecla na janela de 'ROI Cortada' para continuar.")
            cv2.waitKey(0)
            cv2.destroyWindow("ROI Cortada")

            salvar = input("Deseja salvar a ROI? (s/n): ").strip().lower()
            if salvar == 's':
                nome_arquivo = input("Digite o nome do arquivo para salvar (ex.: roi_frame.jpg): ").strip()
                cv2.imwrite(nome_arquivo, roi_cortada)
                print(f"ROI salva como '{nome_arquivo}'")

    cap.release()
    cv2.destroyAllWindows()