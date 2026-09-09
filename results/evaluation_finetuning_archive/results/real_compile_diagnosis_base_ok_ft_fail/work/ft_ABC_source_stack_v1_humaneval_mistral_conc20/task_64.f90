program main
  implicit none
  character(len=100) :: s
  integer :: count
  integer :: i
  character(len=1) :: c

  ! Read input string
  read(*, '(A)') s

  ! Initialize count
  count = 0

  ! Loop through each character
  do i = 1, len(s)
    c = s(i:i)
    ! Check if character is a vowel (case insensitive)
    if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
        c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U') then
      count = count + 1
    else if (c == 'y' .or. c == 'Y') then
      ! 'y' is a vowel only at the end of the word
      if (i == len(s)) then
        count = count + 1
      end if
    end if
  end do

  ! Output the count
  print *, count

end program main