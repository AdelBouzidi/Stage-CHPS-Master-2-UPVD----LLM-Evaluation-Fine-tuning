program vowels_count_demo
  implicit none
  character(len=100) :: input_str
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
    character(len=1) :: ch
    count = 0
    do i = 1, len_trim(s)
      ch = s(i:i)
      if (ch == 'a' .or. ch == 'e' .or. ch == 'i' .or. ch == 'o' .or. ch == 'u' .or. &
          ch == 'A' .or. ch == 'E' .or. ch == 'I' .or. ch == 'O' .or. ch == 'U') then
        count = count + 1
      else if (ch == 'y' .or. ch == 'Y') then
        if (i == len_trim(s)) then
          count = count + 1
        end if
      end if
    end do
  end function vowels_count
end program vowels_count_demo