program vowels_count_demo
  implicit none
  character(len=*) :: input_str
  integer :: result

  read *, input_str
  result = vowels_count(input_str)
  print *, result

contains

  function vowels_count(s) result(count)
    implicit none
    character(len=*), intent(in) :: s
    integer :: count
    integer :: i
    character(len=1) :: c

    count = 0
    do i = 1, len_trim(s)
      c = s(i:i)
      if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
          c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U' .or. &
          (c == 'y' .or. c == 'Y' .and. i == len_trim(s))) then
        count = count + 1
      end if
    end do
  end function vowels_count

end program vowels_count_demo