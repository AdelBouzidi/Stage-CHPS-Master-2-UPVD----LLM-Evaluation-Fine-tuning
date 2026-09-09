program vowels_count_demo
  implicit none
  character(len=*) :: input_string
  integer :: result

  read(*, '(a)') input_string
  result = vowels_count(input_string)
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
      if (char == 'a' .or. char == 'e' .or. char == 'i' .or. char == 'o' .or. char == 'u' .or. &
          char == 'A' .or. char == 'E' .or. char == 'I' .or. char == 'O' .or. char == 'U') then
        count = count + 1
      else if (char == 'y' .or. char == 'Y') then
        if (i == len_trim(s)) then
          count = count + 1
        end if
      end if
    end do
  end function vowels_count

end program vowels_count_demo