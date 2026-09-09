program vowels_count_demo
  implicit none
  character(len=*), parameter :: input_str = "abcde"
  integer :: result

  result = vowels_count(input_str)
  print *, result

contains

  function vowels_count(s) result(count)
    implicit none
    character(len=*), intent(in) :: s
    integer :: count
    integer :: i
    character(len=1) :: char

    count = 0
    do i = 1, len_trim(s)
      char = s(i:i)
      if (ichar(char) >= ichar('a') .and. ichar(char) <= ichar('z')) then
        if (ichar(char) == ichar('a') .or. ichar(char) == ichar('e') .or. &
            ichar(char) == ichar('i') .or. ichar(char) == ichar('o') .or. &
            ichar(char) == ichar('u') .or. (ichar(char) == ichar('y') .and. i == len_trim(s))) then
          count = count + 1
        end if
      end if
    end do
  end function vowels_count

end program vowels_count_demo