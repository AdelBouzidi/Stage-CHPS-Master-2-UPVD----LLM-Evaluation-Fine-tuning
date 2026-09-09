program vowels_count_demo
  implicit none
  character(len=5) :: s
  integer :: count

  s = 'abcde'
  count = vowels_count(s)
  print *, count

contains

  function vowels_count(s) result(count)
    implicit none
    character(len=*), intent(in) :: s
    integer :: count
    integer :: i, len
    character(len=1) :: c

    count = 0
    len = len_trim(s)
    do i = 1, len
      c = s(i:i)
      if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
          c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U') then
        count = count + 1
      else if (c == 'y' .or. c == 'Y') then
        if (i == len) then
          count = count + 1
        end if
      end if
    end do
  end function vowels_count

end program vowels_count_demo